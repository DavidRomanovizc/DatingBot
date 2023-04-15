import asyncio
import os

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import quote_html
from loguru import logger

from functions.main_app.auxiliary_tools import choice_gender, saving_normal_photo, saving_censored_photo
from functions.main_app.determin_location import Location
from keyboards.default.get_location_default import location_keyboard
from keyboards.default.get_photo import get_photo_from_profile
from keyboards.inline.change_data_profile_inline import gender_keyboard
from keyboards.inline.registration_inline import second_registration_keyboard, about_yourself_keyboard
from loader import dp, client, _
from states.reg_state import RegData
from utils.NudeNet.predictor import classification_image, generate_censored_image
from utils.db_api import db_commands
from utils.misc.profanityFilter import censored_message


@dp.callback_query_handler(text='registration')
async def registration(call: CallbackQuery):
    telegram_id = call.from_user.id
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_status = user.get("status")
    if not user_status:
        markup = await second_registration_keyboard()
        text = _("Пройдите опрос, чтобы зарегистрироваться")
        await call.message.edit_text(text, reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="⬆️ Изменить анкету", callback_data="change_profile"))
        await call.message.edit_text(
            "Вы уже зарегистрированы, если вам нужно изменить анкету, то нажмите на кнопку ниже",
            reply_markup=markup)


@dp.callback_query_handler(text_contains="survey")
async def survey(call: CallbackQuery):
    markup = await gender_keyboard()

    await call.message.edit_text(_("Выберите пол"), reply_markup=markup)
    await RegData.sex.set()


@dp.callback_query_handler(state=RegData.sex)
async def sex_reg(call: CallbackQuery):
    if call.data == "male":
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex="Мужской")
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == "female":
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex="Женский")
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)

    await call.message.edit_text(_("Теперь выберите, как вы хотите рассказать о себе:\n"),
                                 reply_markup=await about_yourself_keyboard())
    await RegData.commentary.set()


@dp.callback_query_handler(state=RegData.commentary, text="send_voice")
async def commentary_voice_reg(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(_("Запишите голосовое сообщение"))
    await state.set_state("sending voice")


@dp.message_handler(content_types=[ContentType.VOICE], state="sending voice")
async def voice_reg(message: types.Message, state: FSMContext):
    markup = await gender_keyboard()
    voice_message_id = message.voice.file_id
    try:
        await db_commands.update_user_data(voice_id=voice_message_id, telegram_id=message.from_user.id)
        await message.answer(_("Комментарий принят! Выберите, кого вы хотите найти: "), reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла неизвестная ошибка! Попробуйте изменить комментарий позже в разделе "
                               "\"Меню\"\n\n"
                               "Выберите, кого вы хотите найти: "), reply_markup=markup)
    await RegData.need_partner_sex.set()


@dp.callback_query_handler(state=RegData.commentary, text="send_text")
async def commentary_voice_reg(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(_("Отправьте сообщение о себе"))
    await state.set_state("sending_text")


@dp.message_handler(content_types=[ContentType.TEXT], state="sending_text")
async def commentary_reg(message: types.Message):
    markup = await gender_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(commentary=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(_('Комментарий принят! Выберите, кого вы хотите найти: '), reply_markup=markup)

    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла неизвестная ошибка! Попробуйте изменить комментарий позже в разделе "
                               "\"Меню\"\n\n"
                               "Выберите, кого вы хотите найти: "), reply_markup=markup)
    await RegData.need_partner_sex.set()


@dp.callback_query_handler(state=RegData.need_partner_sex)
async def sex_reg(call: CallbackQuery):
    await choice_gender(call)
    await call.message.edit_text(_("Отлично! Теперь напишите мне ваше имя, которое будут все видеть в анкете"))
    await RegData.name.set()


@dp.message_handler(state=RegData.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(telegram_id=message.from_user.id, varname=quote_html(censored))

    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer(_("Введите сколько вам лет:"))
    await RegData.age.set()


@dp.message_handler(state=RegData.age)
async def get_age(message: types.Message, state: FSMContext):
    markup = await location_keyboard()
    await state.update_data(age=message.text)
    try:
        if 0 < int(message.text) < 110:
            await db_commands.update_user_data(telegram_id=message.from_user.id, age=int(message.text))
        else:
            await message.answer(_("Вы ввели недопустимое число, попробуйте еще раз"))
            return
    except Exception as err:
        logger.error(err)
        await message.answer(_("Вы ввели не число"))
        return
    await message.answer(text=_("Введите город в котором проживаете.\n"
                                "Для точного определения местоположения, можете нажать на кнопку ниже!"),
                         reply_markup=markup)
    await RegData.town.set()


@dp.message_handler(state=RegData.town)
async def get_city(message: types.Message):
    try:
        loc = await Location(message=message)
        await loc.det_loc_in_registration(message)
    except Exception as err:
        await message.answer(_("Произошла неизвестная ошибка! Попробуйте еще раз.\n"
                               "Вероятнее всего вы ввели город неправильно"))
        logger.error(err)


@dp.callback_query_handler(text="yes_all_good", state=RegData.town)
async def get_hobbies(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(_("И напоследок, Пришлите мне вашу фотографию"),
                              reply_markup=await get_photo_from_profile())
    await RegData.photo.set()


@dp.message_handler(content_types=['location'], state=RegData.town)
async def fill_form(message: types.Message):
    try:
        x = message.location.longitude
        y = message.location.latitude
        address = await client.address(f"{x}", f"{y}")
        address = address.split(",")[0:2]
        address = ",".join(address)
        await db_commands.update_user_data(telegram_id=message.from_user.id, city=address)
        await db_commands.update_user_data(telegram_id=message.from_user.id, longitude=x)
        await db_commands.update_user_data(telegram_id=message.from_user.id, latitude=y)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_city=address)
    except Exception as err:
        logger.error(err)
    await asyncio.sleep(1)

    await message.answer(_("И напоследок, Пришлите мне вашу фотографию"), reply_markup=await get_photo_from_profile())
    await RegData.photo.set()


@dp.message_handler(state=RegData.photo)
async def get_photo_profile(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    profile_pictures = await dp.bot.get_user_profile_photos(telegram_id)
    try:
        file_id = dict((profile_pictures.photos[0][0])).get("file_id")
        await saving_normal_photo(message, telegram_id, file_id, state)
    except IndexError:
        await message.answer(_("Произошла ошибка, проверьте настройки конфиденциальности"))


@dp.message_handler(content_types=ContentType.PHOTO, state=RegData.photo)
async def get_photo(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    file_name = f"{str(telegram_id)}.jpg"
    file_id = message.photo[-1].file_id
    censored_file_name = f"{str(message.from_user.id)}_censored.jpg"
    path = f"photos/{file_name}"
    out_path = f"photos/{censored_file_name}"
    await message.photo[-1].download(path)
    data = await classification_image(path)
    safe, unsafe = data.get(path).get("safe"), data.get(path).get("unsafe")
    if safe > 0.8 and unsafe < 0.2:
        await saving_normal_photo(message, telegram_id, file_id, state)
        os.remove(path)
    else:
        await generate_censored_image(image_path=path,
                                      out_path=out_path)
        await saving_censored_photo(message, telegram_id, state, out_path)
        os.remove(path)
        os.remove(out_path)
