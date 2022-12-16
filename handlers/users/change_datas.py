import asyncio
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from aiogram.utils.markdown import quote_html
from loguru import logger

from functions.auxiliary_tools import determining_location
from functions.get_data_func import get_data
from handlers.users.back_handler import delete_message
from keyboards.inline.change_data_profile_inline import change_info_keyboard, gender_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp, _
from states.new_data_state import NewData
from utils.db_api import db_commands
from utils.misc.profanityFilter import censored_message


@dp.callback_query_handler(text='change_profile')
async def start_change_data(call: CallbackQuery):
    markup = await change_info_keyboard()
    await delete_message(call.message)
    await call.message.answer(_("Выберите, что вы хотите изменить: "), reply_markup=markup)


@dp.callback_query_handler(text='name')
async def change_name(call: CallbackQuery):
    await call.message.edit_text(_("Введите новое имя"))
    await NewData.name.set()


@dp.message_handler(state=NewData.name)
async def change_name(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(varname=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(_("Ваше новое имя: <b>{censored}</b>").format(censored=censored))
        await message.answer(_("Выберите, что вы хотите изменить: "), reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла неизвестная ошибка. Попробуйте ещё раз"), reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='age')
async def change_age(call: CallbackQuery):
    await call.message.edit_text(_("Введите новый возраст"))
    await NewData.age.set()


@dp.message_handler(state=NewData.age)
async def change_age(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        if int(message.text) and 0 < int(message.text) < 110:
            await db_commands.update_user_data(age=int(message.text), telegram_id=message.from_user.id)
            await message.answer(_("Ваш новый возраст: <b>{messages}</b>").format(messages=message.text))
            await asyncio.sleep(3)
            await message.answer(_("Выберите, что вы хотите изменить: "), reply_markup=markup)
            await state.reset_state()
        else:
            await message.answer(_("Вы ввели недопустимое число, попробуйте еще раз"))
            return

    except ValueError:
        await message.answer(_("Вы ввели недопустимое число, попробуйте еще раз"))
        return

    await state.reset_state()


@dp.callback_query_handler(text='city')
async def change_city(call: CallbackQuery):
    await call.message.edit_text(_("Введите новый город"))
    await NewData.city.set()


@dp.message_handler(state=NewData.city)
async def change_city(message: types.Message):
    try:
        await determining_location(message, flag=True)
    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла неизвестная ошибка. Попробуйте ещё раз"),
                             reply_markup=await change_info_keyboard())


@dp.callback_query_handler(text="yes_all_good", state=NewData.city)
async def get_hobbies(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(_("Данные успешно изменены.\nВыберите, что вы хотите изменить: "),
                                 reply_markup=await change_info_keyboard())
    await state.reset_state()


@dp.callback_query_handler(text='gender')
async def change_sex(call: CallbackQuery):
    markup = await gender_keyboard()
    await call.message.edit_text(_("Выберите новый пол: "), reply_markup=markup)
    await NewData.sex.set()


@dp.callback_query_handler(state=NewData.sex)
async def change_sex(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    if call.data == 'male':
        try:
            await db_commands.update_user_data(sex="Мужской", telegram_id=call.from_user.id)
            await call.message.edit_text(_("Ваш новый пол: <b>Мужской</b>"))
            await asyncio.sleep(3)
            await call.message.edit_text(_("Выберите, что вы хотите изменить: "), reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(_("Произошла неизвестная ошибка. Попробуйте ещё раз"), reply_markup=markup)
            await state.reset_state()
    if call.data == 'female':
        try:
            await db_commands.update_user_data(sex='Женский', telegram_id=call.from_user.id)
            await call.message.edit_text(_("Ваш новый пол: <b>Женский</b>"))
            await asyncio.sleep(3)
            await call.message.edit_text(_("Выберите, что вы хотите изменить: "), reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(_("Произошла неизвестная ошибка. Попробуйте ещё раз"), reply_markup=markup)
            await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='photo')
async def new_photo(call: CallbackQuery):
    await call.message.edit_text(_("Отправьте мне новую фотографию"))
    await NewData.photo.set()
    await asyncio.sleep(3)
    await delete_message(call.message)


@dp.message_handler(content_types=ContentType.PHOTO, state=NewData.photo)
async def update_photo_complete(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    file_id = message.photo[-1].file_id
    try:
        await db_commands.update_user_data(photo_id=file_id, telegram_id=message.from_user.id)
        await message.answer(_("Фото принято!"))
        await asyncio.sleep(3)
        await delete_message(message)
        await message.answer(_("Выберите, что вы хотите изменить: "), reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n"
                               "Если ошибка осталась, напишите системному администратору."))
        await state.reset_state()


@dp.callback_query_handler(text='about_me')
async def new_comment(call: CallbackQuery):
    user_data = await get_data(call.from_user.id)
    if user_data[11] is None:
        await call.message.edit_text(_("Отправьте мне новое описание анкеты:"))
    else:
        await call.message.edit_text(_("Отправьте голосовое сообщение"))
    await NewData.commentary.set()


@dp.message_handler(content_types=[ContentType.VOICE], state=NewData.commentary)
async def voice_reg(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    voice_message_id = message.voice.file_id
    try:
        await db_commands.update_user_data(voice_id=voice_message_id, telegram_id=message.from_user.id)
        await message.answer(_("Комментарий принят!"))
        await asyncio.sleep(1)
        await delete_message(message)
        await message.answer(_("Выберите, что вы хотите изменить: "), reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла неизвестная ошибка! Попробуйте изменить комментарий позже в разделе "
                               "\"Меню\"\n\n"
                               "Выберите, кого вы хотите найти: "), reply_markup=markup)
    await state.reset_state()


@dp.message_handler(state=NewData.commentary)
async def update_comment_complete(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(commentary=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(_("Комментарий принят!"))
        await asyncio.sleep(3)
        await delete_message(message)
        await message.answer(_("Выберите, что вы хотите изменить: "), reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла ошибка! Попробуйте еще раз изменить описание. "
                               "Возможно, Ваше сообщение слишком большое\n"
                               "Если ошибка осталась, напишите системному администратору."))
        await state.reset_state()


@dp.callback_query_handler(text="add_inst")
async def add_inst(call: CallbackQuery, state: FSMContext):
    await delete_message(call.message)
    await call.message.answer(_("Напишите имя своего аккаунта\n\n"
                                "Примеры:\n"
                                "<code>@unknown</code>\n"
                                "<code>https://www.instagram.com/unknown</code>"))
    await state.set_state("inst")


@dp.message_handler(state="inst")
async def add_inst_state(message: types.Message, state: FSMContext):
    try:
        user_db = await db_commands.select_user(telegram_id=message.from_user.id)
        markup = await start_keyboard(user_db["status"])
        inst_regex = r"([A-Za-z0-9._](?:(?:[A-Za-z0-9._]|(?:\.(?!\.))){2,28}(?:[A-Za-z0-9._]))?)$"
        regex = re.search(inst_regex, message.text)
        result = regex
        if bool(regex):
            await state.update_data(inst=message.text)
            await db_commands.update_user_data(instagram=result[0], telegram_id=message.from_user.id)
            await message.answer(_("Ваш аккаунт успешно добавлен"))
            await state.reset_state()
            await message.answer(_("Вы были возвращены в меню"), reply_markup=markup)
        else:
            await message.answer(_("Вы ввели неправильную ссылку или имя аккаунта.\n\nПримеры:\n"
                                   "<code>@unknown</code>\n<code>https://www.instagram.com/unknown</code>"))

    except Exception as err:
        logger.error(err)
        await message.answer(_("Возникла ошибка. Попробуйте еще раз"))
