import asyncio

from loguru import logger

from handlers.users.back_handler import delete_message
from keyboards.inline.change_inline import gender_keyboard
from keyboards.inline.change_data_profile_inline import change_info_keyboard

from aiogram.types import CallbackQuery, ContentType

from states.new_data_state import NewData
from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram import types

from utils.db_api import db_commands


@dp.callback_query_handler(text='change_profile')
async def start_change_data(call: CallbackQuery):
    markup = await change_info_keyboard()
    await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)


@dp.callback_query_handler(text='name')
async def change_name(call: CallbackQuery):
    await call.message.edit_text(f'Введите новое имя')
    await NewData.name.set()


@dp.message_handler(state=NewData.name)
async def change_name(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db_commands.update_user_data(varname=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Ваше новое имя: <b>{message.text}</b>')
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка',
                             reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='age')
async def change_age(call: CallbackQuery):
    await call.message.edit_text(f'Введите новый возраст')
    await NewData.age.set()


@dp.message_handler(state=NewData.age)
async def change_age(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db_commands.update_user_data(age=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Ваш новый возраст: <b>{message.text}</b>')
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()

    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='city')
async def change_city(call: CallbackQuery):
    await call.message.edit_text(f'Введите новый город')
    await NewData.city.set()


@dp.message_handler(state=NewData.city)
async def change_city(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db_commands.update_user_data(city=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Ваш новый город: <b>{message.text}</b>')
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='gender')
async def change_sex(call: CallbackQuery):
    markup = await gender_keyboard()
    await call.message.edit_text(f'Выберите новый пол: ', reply_markup=markup)
    await NewData.sex.set()


@dp.callback_query_handler(state=NewData.sex)
async def change_sex(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    if call.data == 'male':
        try:
            await db_commands.update_user_data(sex='Мужской', telegram_id=call.from_user.id)
            await call.message.edit_text(f'Ваш новый пол: <b>Мужской</b>')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
            await state.reset_state()
    if call.data == 'female':
        try:
            await db_commands.update_user_data(sex='Женский', telegram_id=call.from_user.id)
            await call.message.edit_text(f'Ваш новый пол: <b>Женский</b>')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
            await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='busyness')
async def change_style(call: CallbackQuery):
    await call.message.edit_text(f'Чем вы занимаетесь?')
    await NewData.hobbies.set()


@dp.message_handler(state=NewData.hobbies)
async def change_style(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db_commands.update_user_data(lifestyle=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Данные были изменены!')
        await asyncio.sleep(3)
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка', reply_markup=markup)
        await state.reset_state()
    await state.reset_state()


@dp.callback_query_handler(text='photo')
async def new_photo(call: CallbackQuery):
    await call.message.edit_text(f'Отправьте мне новую фотографию')
    await NewData.photo.set()
    await asyncio.sleep(5)
    await delete_message(call.message)


@dp.message_handler(content_types=ContentType.PHOTO, state=NewData.photo)
async def update_photo_complete(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    file_id = message.photo[-1].file_id
    try:
        await db_commands.update_user_data(photo_id=file_id, telegram_id=message.from_user.id)
        await message.answer(f'Фото принято!')
        await asyncio.sleep(3)
        await delete_message(message)
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n'
                             f'Если ошибка осталась, напишите системному администратору.')
        await state.reset_state()


@dp.callback_query_handler(text='about_me')
async def new_comment(call: CallbackQuery):
    await call.message.edit_text(f'Отправьте мне новое описание анкеты: ')
    await NewData.commentary.set()


@dp.message_handler(state=NewData.commentary)
async def update_comment_complete(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db_commands.update_user_data(commentary=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Комментарий принят!')
        await asyncio.sleep(3)
        await delete_message(message)
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла ошибка! Попробуйте еще раз изменить описание. '
                             f'Возможно, Ваше сообщение слишком большое\n'
                             f'Если ошибка осталась, напишите системному администратору.')
        await state.reset_state()
