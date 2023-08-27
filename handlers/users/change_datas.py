import asyncio
import os
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from aiogram.utils.markdown import quote_html
from django.db import DataError

from functions.main_app.auxiliary_tools import (
    update_normal_photo,
    saving_censored_photo,
)
from functions.main_app.determin_location import Location, RegistrationStrategy
from handlers.users.back import delete_message
from keyboards.default.get_photo import get_photo_from_profile
from keyboards.inline.change_data_profile_inline import (
    change_info_keyboard,
    gender_keyboard,
)
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp, _, logger
from states.new_data_state import NewData
from utils.NudeNet.predictor import classification_image, generate_censored_image
from utils.YandexMap.exceptions import NothingFound
from utils.db_api import db_commands
from utils.misc.profanityFilter import censored_message


@dp.callback_query_handler(text="change_profile")
async def start_change_data(call: CallbackQuery) -> None:
    markup = await change_info_keyboard()
    await delete_message(call.message)
    await call.message.answer(text=_("<u>Ваши данные: </u>\n"), reply_markup=markup)


@dp.callback_query_handler(text="name")
async def change_name(call: CallbackQuery) -> None:
    await call.message.edit_text(text=_("Введите новое имя"))
    await NewData.name.set()


@dp.message_handler(state=NewData.name)
async def change_name(message: types.Message, state: FSMContext) -> None:
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(
            varname=quote_html(censored), telegram_id=message.from_user.id
        )
        await message.answer(
            text=_("Ваше новое имя: <b>{censored}</b>\n"
                   "Выберите, что вы хотите изменить: ").format(censored=censored),
            reply_markup=markup
        )
        await state.reset_state()
    except DataError as ex:
        logger.error(f"Error in change_name: {ex}")
        await message.answer(
            text=_(
                "Произошла неизвестная ошибка. Попробуйте ещё раз\n"
                "Возможно, Ваше сообщение слишком большое"
            ),
            reply_markup=markup,
        )
        return

    await state.reset_state()


@dp.callback_query_handler(text="age")
async def change_age(call: CallbackQuery) -> None:
    await call.message.edit_text(text=_("Введите новый возраст"))
    await NewData.age.set()


@dp.message_handler(state=NewData.age)
async def change_age(message: types.Message, state: FSMContext) -> None:
    markup = await change_info_keyboard()
    try:
        if int(message.text) and 10 < int(message.text) < 90:
            await db_commands.update_user_data(
                age=int(message.text), telegram_id=message.from_user.id
            )
            await asyncio.sleep(1)
            await message.answer(
                text=_("Ваш новый возраст: <b>{messages}</b>\n"
                       "Выберите, что вы хотите изменить: ").format(
                    messages=message.text
                ), reply_markup=markup
            )
            await state.reset_state()
        else:
            await message.answer(
                text=_("Вы ввели недопустимое число, попробуйте еще раз")
            )
            return

    except ValueError:
        await message.answer(text=_("Вы ввели не число, попробуйте еще раз"))
        return

    await state.reset_state()


@dp.callback_query_handler(text="city")
async def change_city(call: CallbackQuery) -> None:
    await call.message.edit_text(text=_("Введите новый город"))
    await NewData.city.set()


@dp.message_handler(state=NewData.city)
async def change_city(message: types.Message) -> None:
    try:
        loc = await Location(message=message, strategy=RegistrationStrategy())
        await loc.det_loc()
    except NothingFound as ex:
        logger.error(f"Error in change_city. {ex}")
        await message.answer(
            text=_("Мы не смогли найти город {city}. Попробуйте ещё раз").format(
                city=message.text
            )
        )
        return


@dp.callback_query_handler(text="yes_all_good", state=NewData.city)
async def get_hobbies(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        text=_("Данные успешно изменены.\n" "Выберите, что вы хотите изменить: "),
        reply_markup=await change_info_keyboard(),
    )
    await state.reset_state()


@dp.callback_query_handler(text="gender")
async def change_sex(call: CallbackQuery) -> None:
    markup = await gender_keyboard(
        m_gender=_("👱🏻‍♂️ Мужской"), f_gender=_("👱🏻‍♀️ Женский")
    )
    await call.message.edit_text(text=_("Выберите новый пол: "), reply_markup=markup)
    await NewData.sex.set()


@dp.callback_query_handler(state=NewData.sex)
async def change_sex(call: CallbackQuery, state: FSMContext) -> None:
    markup = await change_info_keyboard()
    gender = "Мужской" if call.data == "male" else "Женский"
    await db_commands.update_user_data(sex=gender, telegram_id=call.from_user.id)
    await call.message.edit_text(
        text=_("Ваш новый пол: <b>{}</b>\n"
               "Выберите, что вы хотите изменить: ").format(gender),
        reply_markup=markup
    )
    await state.reset_state()


@dp.callback_query_handler(text="photo")
async def new_photo(call: CallbackQuery) -> None:
    await delete_message(call.message)
    await call.message.answer(
        text=_("Отправьте мне новую фотографию"),
        reply_markup=await get_photo_from_profile(),
    )
    await NewData.photo.set()
    await asyncio.sleep(1)
    await delete_message(call.message)


@dp.message_handler(state=NewData.photo)
async def get_photo_profile(message: types.Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id
    markup = await change_info_keyboard()
    profile_pictures = await dp.bot.get_user_profile_photos(telegram_id)
    try:
        file_id = dict((profile_pictures.photos[0][0])).get("file_id")
        await update_normal_photo(
            message=message,
            telegram_id=telegram_id,
            file_id=file_id,
            state=state,
            markup=markup,
        )
    except IndexError:
        await message.answer(
            text=_("Произошла ошибка, проверьте настройки конфиденциальности")
        )


@dp.message_handler(content_types=ContentType.PHOTO, state=NewData.photo)
async def update_photo_complete(message: types.Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id
    markup = await change_info_keyboard()
    file_name = f"{str(telegram_id)}.jpg"
    file_id = message.photo[-1].file_id
    censored_file_name = f"{str(message.from_user.id)}_censored.jpg"
    path, out_path = f"photos/{file_name}", f"photos/{censored_file_name}"
    await message.photo[-1].download(path)
    data = await classification_image(path)
    safe, unsafe = data.get(path).get("safe"), data.get(path).get("unsafe")
    if safe > 0.6 or unsafe < 0.2:
        await update_normal_photo(
            message=message,
            telegram_id=telegram_id,
            file_id=file_id,
            state=state,
            markup=markup,
        )
        os.remove(path)
    else:
        await generate_censored_image(image_path=path, out_path=out_path)
        await saving_censored_photo(
            message=message,
            telegram_id=telegram_id,
            state=state,
            out_path=out_path,
            markup=markup,
            flag="change_datas",
        )
        os.remove(path)
        await asyncio.sleep(0.2)
        os.remove(out_path)


@dp.callback_query_handler(text="about_me")
async def new_comment(call: CallbackQuery) -> None:
    await call.message.edit_text(text=_("Отправьте сообщение о себе"))
    await NewData.commentary.set()


@dp.message_handler(state=NewData.commentary)
async def update_comment_complete(message: types.Message, state: FSMContext) -> None:
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(
            commentary=quote_html(censored), telegram_id=message.from_user.id
        )
        await asyncio.sleep(0.2)
        await delete_message(message)
        await message.answer(
            text=_("Комментарий принят!\n"
                   "Выберите, что вы хотите изменить: "), reply_markup=markup
        )
        await state.reset_state()
    except DataError as ex:
        logger.error(f"Error in update_comment_complete {ex}")
        await message.answer(
            text=_(
                "Произошла ошибка! Попробуйте еще раз изменить описание. "
                "Возможно, Ваше сообщение слишком большое\n"
                "Если ошибка осталась, напишите в поддержку."
            )
        )
        return


@dp.callback_query_handler(text="add_inst")
async def add_inst(call: CallbackQuery, state: FSMContext) -> None:
    await delete_message(call.message)
    await call.message.answer(
        text=_(
            "Напишите имя своего аккаунта\n\n"
            "Примеры:\n"
            "<code>@unknown</code>\n"
            "<code>https://www.instagram.com/unknown</code>"
        )
    )
    await state.set_state("inst")


@dp.message_handler(state="inst")
async def add_inst_state(message: types.Message, state: FSMContext) -> None:
    try:
        markup = await start_keyboard(obj=message)
        inst_regex = r"([A-Za-z0-9._](?:(?:[A-Za-z0-9._]|(?:\.(?!\.))){2,28}(?:[A-Za-z0-9._]))?)$"
        regex = re.search(inst_regex, message.text)
        result = regex
        if bool(regex):
            await state.update_data(inst=message.text)
            await db_commands.update_user_data(
                instagram=result[0], telegram_id=message.from_user.id
            )
            await message.answer(text=_("Ваш аккаунт успешно добавлен"))
            await asyncio.sleep(1)
            await state.reset_state()
            await message.answer(
                text=_("Вы были возвращены в меню"), reply_markup=markup
            )
        else:
            await message.answer(
                text=_(
                    "Вы ввели неправильную ссылку или имя аккаунта.\n\nПримеры:\n"
                    "<code>@unknown</code>\n<code>https://www.instagram.com/unknown</code>"
                )
            )

    except DataError:
        await message.answer(text=_("Возникла ошибка. Попробуйте еще раз"))
        return
