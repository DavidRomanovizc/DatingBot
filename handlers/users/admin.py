from keyboards.inline.admin_inline import admin_mode_keyboard, approval_keyboard, find_user
from keyboards.inline.main_menu_inline import start_keyboard
from aiogram.utils.exceptions import UserDeactivated
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from utils.db_api import db_commands
from data.config import ADMINS
from filters import IsPrivate
from loader import dp, bot
from loguru import logger
from asyncio import sleep
from aiogram import types


@dp.message_handler(IsPrivate(), chat_id=ADMINS, text="/admin")
async def open_admin_mode(message: types.Message):
    markup = await admin_mode_keyboard()
    await message.answer(f"Приветствую, мой повелитель! Вот мои функции: ", reply_markup=markup)


@dp.callback_query_handler(text="mailing_start")
async def mailing_start(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.from_user.id, "Отправьте сообщение для рассылки")
    await state.set_state("mailing")


@dp.message_handler(state="mailing")
async def send_mailing(message: types.Message, state: FSMContext):
    answer = message.text
    count_users = await db_commands.count_users()
    markup = await approval_keyboard()
    async with state.proxy() as data:
        data['mailing'] = answer
    await message.answer(f'Отправьте любое сообщение для подтверждения отправки следующего сообщения: \n\n'
                         f'<b>{answer}</b>\n\n'
                         f'Сообщение получат: <b>{count_users}</b> человек', parse_mode='HTML', reply_markup=markup)
    await state.set_state("mailing_2")


@dp.callback_query_handler(text="approved_btn", state="mailing_2")
async def mailing_final(call: CallbackQuery, state: FSMContext):
    data1 = await state.get_data()
    answer1 = str(data1.get('mailing'))
    users = await db_commands.select_all_users()
    for i in users:
        id_chat = i.get('telegram_id')
        await bot.send_message(chat_id=id_chat, text=f'Вы получили следующую рассылку: \n\n'
                                                     f'{answer1}\n\n')
        await sleep(0.5)

    await state.reset_state(with_data=True)


@dp.callback_query_handler(text='show_active_users')
async def count_users_db(call: CallbackQuery):
    count_users = await db_commands.count_users()
    await call.answer(text=f'В боте зарегистрировано {count_users} участников', show_alert=True)


@dp.callback_query_handler(text="find_users")
async def start_find(call: CallbackQuery):
    markup = await find_user()
    await call.message.edit_text("Выберите способ поиска пользователя", reply_markup=markup)


@dp.callback_query_handler(text="find_id")
async def send_find(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Напишите ID пользователя")
    await state.set_state("ID")


@dp.message_handler(state="ID")
async def send_find(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['id'] = answer
    data = await state.get_data()
    telegram_id = data.get('id')
    try:
        user = await db_commands.select_user(telegram_id=telegram_id)
        full_name = user.get("full_name")
        username = user.get("username")
        user_balance = user.get("balance")
        user_created = user.get("created_at")
        user_created = user_created.strftime("%b %d %Y %H:%M:%S")
        markup = await start_keyboard()
        await message.answer(f'<b>Пользователь найден, вот данные о нем:</b>\n\n'
                             f'<b>Имя:</b> {full_name}\n\n'
                             f'<b>Ссылка:</b> https://t.me/{username}\n'
                             f'<b>Баланс:</b> {user_balance}$\n\n'
                             f'<b>Дата регистрации:</b> <code>{user_created}</code>\n\n')
        await message.answer("Главное меню", reply_markup=markup)
    except Exception as err:
        logger.error(err)
        await message.answer(f'Пользователь не найден, попробуйте изменить ID')

    await state.reset_state(with_data=True)


@dp.callback_query_handler(text="find_user")
async def send_find(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Напишите username пользователя")
    await state.set_state("username_get")


@dp.message_handler(state="username_get")
async def send_find(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['name'] = answer
    data = await state.get_data()
    username = data.get('name')
    try:
        user = await db_commands.select_user_username(username=username)
        full_name = user.get("full_name")
        telegram_id = user.get("telegram_id")
        user_balance = user.get("balance")
        user_created = user.get("created_at")
        user_created = user_created.strftime("%b %d %Y %H:%M:%S")
        await message.answer(f'<b>Пользователь найден, вот данные о нем:</b>\n\n'
                             f'Имя: {full_name}\n\n'
                             f'<b>Телеграм ID:</b> {telegram_id}\n\n'
                             f'<b>Ссылка:</b> https://t.me/{username}\n'
                             f'<b>Баланс:</b> {user_balance}$\n\n'
                             f'<b>Дата регистрации:</b> <code>{user_created}</code>\n\n')
    except UserDeactivated:
        await message.answer(f'Пользователь не найден, попробуйте изменить ID')

    await state.reset_state(with_data=True)


@dp.callback_query_handler(text='ban_user_id')
async def get_ban_id(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text="Отправьте ID пользователя, которого нужно забанить")
    await state.set_state("get_ban_id")


@dp.message_handler(state="get_ban_id")
async def complete_ban(message: types.Message, state: FSMContext):
    try:
        user_id = message.text
        await db_commands.update_user_data(telegram_id=user_id, is_banned=True)
        await message.answer(text="Пользователь успешно забанен!")
    except Exception as err:
        logger.critical(err)
        await message.answer(text="Не удалось забанить юзера - проверьте введенные данные")

    await state.reset_state(with_data=True)
