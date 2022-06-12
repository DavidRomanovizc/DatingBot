import asyncio
import re

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import quote_html
from loguru import logger

from keyboards.default.get_location_default import location_keyboard
from keyboards.inline.change_data_profile_inline import gender_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.registration_inline import second_registration_keyboard

from loader import dp, client
from states.reg_state import RegData

from utils.db_api import db_commands
from functions.get_data_func import get_data
from utils.misc.profanityFilter import censored_message


@dp.callback_query_handler(text='registration')
async def registration(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    user_status = user_data[9]
    if not user_status:
        markup = await second_registration_keyboard()
        text = f"Пройдите опрос, чтобы зарегистрироваться"
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

    await call.message.edit_text("Выберите пол", reply_markup=markup)
    await RegData.sex.set()


@dp.callback_query_handler(state=RegData.sex)
async def sex_reg(call: CallbackQuery):
    if call.data == 'male':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex="Мужской")
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'female':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex='Женский')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)

    await call.message.edit_text(f'Теперь напишите немного о себе: \n\n(255 символов max.)')
    await RegData.commentary.set()


@dp.message_handler(state=RegData.commentary)
async def commentary_reg(message: types.Message):
    markup = await gender_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(commentary=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(f'Комментарий принят! Выберите, кого вы хотите найти: ', reply_markup=markup)


    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка! Попробуйте изменить комментарий позже в разделе '
                             f'"Меню"\n\n'
                             f'Выберите, кого вы хотите найти: ', reply_markup=markup)
    await RegData.need_partner_sex.set()


@dp.callback_query_handler(state=RegData.need_partner_sex)
async def sex_reg(call: CallbackQuery):
    if call.data == 'male':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, need_partner_sex='Мужской')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'female':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, need_partner_sex='Женский')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)

    await call.message.edit_text(f'Отлично! Теперь напишите мне ваше имя, которое будут все видеть в анкете')
    await RegData.name.set()


@dp.message_handler(state=RegData.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(telegram_id=message.from_user.id, varname=quote_html(censored))

    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Введите сколько вам лет:")
    await RegData.age.set()


@dp.message_handler(state=RegData.age)
async def get_age(message: types.Message, state: FSMContext):
    markup = await location_keyboard()
    await state.update_data(age=message.text)
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(telegram_id=message.from_user.id, age=quote_html(censored))
    except Exception as err:
        logger.error(err)
        await message.answer("Вы ввели не число")
        return
    await message.answer(text="Введите город в котором проживаете.\n"
                              "Для точного определения местоположения, можете нажать на кнопку ниже!",
                         reply_markup=markup)
    await RegData.town.set()


@dp.message_handler(state=RegData.town)
async def get_city(message: types.Message):
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, city=quote_html(message.text))
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_city=message.text)
    except Exception as err:
        logger.error(err)
    await message.answer("Чем вы занимаетесь:")
    await RegData.hobbies.set()


@dp.message_handler(content_types=['location'], state=RegData.town)
async def fill_form(message: types.Message):
    try:
        x = message.location.longitude
        y = message.location.latitude
        address = client.address(f"{x}", f"{y}")
        first_word = re.findall(r'\w+', address)[1]

        await db_commands.update_user_data(telegram_id=message.from_user.id, city=first_word)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_city=first_word)
        await db_commands.update_user_data(telegram_id=message.from_user.id, longitude=x)
        await db_commands.update_user_data(telegram_id=message.from_user.id, latitude=y)
        await message.answer('Ваш город сохранен!')
    except Exception as err:
        logger.error(err)
    await asyncio.sleep(1)
    await message.answer("Чем вы занимаетесь:")
    await RegData.hobbies.set()


@dp.message_handler(state=RegData.hobbies)
async def get_hobbies(message: types.Message, state: FSMContext):
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, lifestyle=quote_html(message.text))
        await state.update_data(hobbies=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer(f"И напоследок, Пришлите мне вашу фотографию")
    await RegData.photo.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=RegData.photo)
async def get_photo(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    file_id = message.photo[-1].file_id
    try:
        await db_commands.update_user_data(telegram_id=telegram_id, photo_id=file_id)

        await message.answer(f'Фото принято!')
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n'
                             f'Если ошибка осталась, напишите системному администратору.')

    await state.finish()
    await db_commands.update_user_data(telegram_id=telegram_id, status=True)

    user_data = await get_data(telegram_id)
    user_db = await db_commands.select_user(telegram_id=telegram_id)
    markup = await start_keyboard(status=user_db['status'])
    await message.answer_photo(caption=f"Регистрация успешно завершена! \n\n "
                                       f"{str(user_data[0])}, "
                                       f"{str(user_data[1])} лет, "
                                       f"{str(user_data[3])}\n\n"
                                       f"<b>О себе</b> - {str(user_data[5])}",
                               photo=user_db.get('photo_id'), reply_markup=ReplyKeyboardRemove())
    await message.answer("Меню: ", reply_markup=markup)
