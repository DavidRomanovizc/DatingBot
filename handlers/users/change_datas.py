import asyncio
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from loguru import logger

from handlers.users.back_handler import delete_message
from keyboards.inline.change_data_profile_inline import change_info_keyboard, gender_keyboard
from keyboards.inline.registration_inline import confirm_keyboard
from keyboards.inline.second_menu_inline import second_menu_keyboard
from loader import dp, client
from states.new_data_state import NewData
from utils.db_api import db_commands
from utils.misc.check_name import mat_validator


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
async def change_city(message: types.Message):
    try:
        markup = await confirm_keyboard()
        x, y = client.coordinates(message.text)
        city = client.address(f"{x}", f"{y}")
        censored = mat_validator(message.text)
        if censored:
            await message.answer(f'Я нашел такой адрес:\n'
                                 f'<b>{city}</b>\n'
                                 f'Если все правильно то подтвердите.', reply_markup=markup)
            await db_commands.update_user_data(telegram_id=message.from_user.id, city=city)
            await db_commands.update_user_data(telegram_id=message.from_user.id, longitude=x)
            await db_commands.update_user_data(telegram_id=message.from_user.id, latitude=y)
        else:
            await message.answer(f"Вы ввели запрещенное слово. Попробуйте ещё раз")
            return
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка. Попробуйте ещё раз',
                             reply_markup=await change_info_keyboard())


@dp.callback_query_handler(text="yes_all_good", state=NewData.city)
async def get_hobbies(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'Данные успешно изменены.\nВыберите, что вы хотите изменить: ',
                                 reply_markup=await change_info_keyboard())
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


@dp.callback_query_handler(text="add_inst")
async def add_inst(call: CallbackQuery, state: FSMContext):
    await delete_message(call.message)
    await call.message.answer("Напишите имя своего аккаунта")
    await state.set_state("inst")


@dp.message_handler(state="inst")
async def add_inst_state(message: types.Message, state: FSMContext):
    try:
        markup = await second_menu_keyboard()
        inst_regex = r"^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$"
        if bool(re.match(pattern=inst_regex, string=message.text)):
            await state.update_data(inst=message.text)
            await db_commands.update_user_data(instagram=message.text, telegram_id=message.from_user.id)
            await message.answer(f"Ваш аккаунт успешно добавлен")
            await state.reset_state()
            await delete_message(message)
            await asyncio.sleep(1)
            await message.answer("Вы были возвращены в меню", reply_markup=markup)
    except Exception as err:
        logger.error(err)
        await message.answer("Возникла ошибка. Попробуйте еще раз")
