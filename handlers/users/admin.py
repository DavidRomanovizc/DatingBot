from keyboards.inline.admin_inline import admin_mode_kb
from states.ban_user_states import BanUser
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from states.find_user import FindUser
from states.mailing import Mailing
from loader import dp, db, bot
from data.config import ADMINS
from asyncio import sleep
from aiogram import types
import asyncpg


@dp.message_handler(chat_id=ADMINS, text='/admin')
async def open_admin_mode(message: types.Message):
    await message.answer(f'Приветствую, мой повелитель! Вот мои функции: ', reply_markup=admin_mode_kb)


@dp.callback_query_handler(text='create_base_users')
async def create_base_users(call: CallbackQuery):
    try:
        await db.create_table_users()
    except:
        await call.answer(f'Ошибка! Вполне возможно, база уже есть', show_alert=True)

    await call.answer(text=f'Таблица пользователей создана со следующими параметрами: \n\n'
                           f'id, fullname, photo, username, email, sex, is_premium, age, '
                           f'national, education, city, car, apartment, marital', show_alert=True)


@dp.callback_query_handler(text='create_base_Payments')
async def create_base_users(call: CallbackQuery):
    try:
        await db.create_table_payments()
    except:
        await call.answer(f'Ошибка! Вполне возможно, база уже есть', show_alert=True)

    await call.answer(text=f'Таблица оплаты создана со следующими параметрами: \n\n'
                           f'id, fullname, is_premium, telegram_id', show_alert=True)


@dp.callback_query_handler(text='mailing_start', state=None)
async def mailing_start(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Отправьте сообщение для рассылки. Это сообщение получат те,'
                                                        ' кто не купил премиум!')
    await Mailing.stage1.set()


@dp.message_handler(state=Mailing.stage1)
async def send_mailing(message: types.Message, state: FSMContext):
    answer = message.text
    count_usersers = await db.count_users()
    async with state.proxy() as data:
        data['mailing'] = answer
    await message.answer(f'Отправьте любое сообщение для подтверждения отправки следующего сообщения: \n\n'
                         f'<b>{answer}</b>\n\n'
                         f'Сообщение получат: <b>{count_usersers}</b> человек', parse_mode='HTML')
    await Mailing.stage2.set()


@dp.message_handler(state=Mailing.stage2)
async def mailing_final(state: FSMContext):
    data1 = await state.get_data()
    answer1 = str(data1.get('mailing'))
    users = await db.select_all_users()
    for i in users:
        id_chat = i.get('telegram_id')
        await bot.send_message(chat_id=id_chat, text=f'Вы получили следующую рассылку: \n\n'
                                                     f'{answer1}\n\n'
                                                     f'Чтобы отказаться от рассылки, купите премиум :)')
        await sleep(0.3)

    await state.reset_state(with_data=True)


@dp.callback_query_handler(text='show_active_users')
async def count_users_db(call: CallbackQuery):
    count_users = await db.count_users()
    await call.answer(text=f'В боте зарегистрировано {count_users} участников', show_alert=True)


@dp.callback_query_handler(text='delete_db')
async def delete_users_db(call: CallbackQuery):
    await db.drop_users()
    await db.drop_payments()
    await bot.send_message(call.from_user.id, f'База данных успешно удалена!')


@dp.callback_query_handler(text='initialization_user')
async def initialize_me(call: CallbackQuery):
    try:
        user = await db.add_user_Users(full_name=call.from_user.full_name,
                                       telegram_id=call.from_user.id,
                                       username=call.from_user.username,
                                       email=None,
                                       sex=None,
                                       national=None,
                                       education=None,
                                       city=None,
                                       age=None,
                                       kids=None,
                                       language=None,
                                       marital=None,
                                       car=None,
                                       varname=None,
                                       lifestyle=None,
                                       is_banned=False,
                                       apartment=None)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=call.from_user.id)
        await bot.send_message(chat_id=user.get('telegram_id'), text=f'С возвращением, {call.from_user.full_name}!')
    await bot.answer_callback_query(call.id)

    user_data = list(user)
    user_data_dict = dict(user)
    username = user.get('username')
    full_name = user[2]
    count_users = await db.count_users()
    await bot.send_message(call.from_user.id, f'Отправляю данные о Вас...')
    await bot.send_message(call.from_user.id, f'Данные следующие: \n\n'
                                              f'Количество юзеров - <b>{count_users}</b>\n\n'
                                              f'Данные о Вас: \n'
                                              f'<code>User - {username}, {full_name}\n'
                                              f'{user_data=}\n'
                                              f'{user_data_dict=}</code>', parse_mode='HTML')


@dp.callback_query_handler(text='find_user')
async def start_find(call: CallbackQuery):
    await bot.send_message(call.from_user.id, f'Введите айди пользователя, которого хотите найти')
    await FindUser.process_find1.set()


@dp.message_handler(state=FindUser.process_find1)
async def delete_users_db(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['id'] = answer
    await bot.send_message(message.from_user.id, f'Отправьте любое сообщение, чтобы продолжать')

    await FindUser.finish_find.set()


@dp.message_handler(state=FindUser.finish_find)
async def delete_users_db(message: types.Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = data.get('id')
    try:
        user = await db.select_user(telegram_id=telegram_id)
        await bot.send_message(message.from_user.id, f'Пользователь найден, вот данные о нем:\n\n'
                                                     f'{list(user)}')
    except:
        await bot.send_message(message.from_user.id, f'Пользователь не найден, попробуйте изменить ID')

    await state.reset_state()


@dp.callback_query_handler(text='ban_user_id')
async def ban_user(call: CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Бан', callback_data='ban')
    keyboard.add(btn1)
    btn1 = types.InlineKeyboardButton(text='Разбан', callback_data='unban')
    keyboard.add(btn1)
    btn1 = types.InlineKeyboardButton(text='Отмена', callback_data='cancel_ban')
    keyboard.add(btn1)
    await bot.send_message(call.from_user.id, f'Выберите функцию: ', reply_markup=keyboard)


@dp.callback_query_handler(text='ban')
async def ban_user(call: CallbackQuery):
    await bot.send_message(call.from_user.id, f'Введите id пользователя, которого нужно <b>ЗАБАНИТЬ</b>')
    await BanUser.ban_complete.set()


@dp.message_handler(state=BanUser.ban_complete)
async def complete_ban(message: types.Message, state: FSMContext):
    need_ban_id = message.text
    try:
        full_name_banned_user = await db.select_user(telegram_id=int(need_ban_id))
    except:
        full_name_banned_user = 0

    fullname = full_name_banned_user.get('full_name')
    try:
        await db.update_user_ban_status(is_banned=True, telegram_id=int(need_ban_id))
        await bot.send_message(message.from_user.id, f'Пользователь {fullname} был успешно забанен!')
        await state.reset_state()
    except:
        await bot.send_message(f'Произошла неизвестная ошибка! Попробуйте изменить id в формате целочисленного числа')
        await state.reset_state()


@dp.callback_query_handler(text='unban')
async def ban_user(call: CallbackQuery):
    await bot.send_message(call.from_user.id, f'Введите id пользователя, которого нужно <b>РАЗБАНИТЬ</b>')
    await BanUser.unban_complete.set()


@dp.message_handler(state=BanUser.unban_complete)
async def complete_unban(message: types.Message, state: FSMContext):
    need_unban_id = message.text
    try:
        full_name_unbanned_user = await db.select_user(telegram_id=int(need_unban_id))
    except:
        full_name_unbanned_user = 0

    fullname = full_name_unbanned_user.get('full_name')
    try:
        await db.update_user_ban_status(is_banned=False, telegram_id=int(need_unban_id))
        await bot.send_message(message.from_user.id, f'Пользователь {fullname} был успешно разбанен!')
        await state.reset_state()
    except:
        await bot.send_message(f'Произошла неизвестная ошибка! Попробуйте изменить id в формате целочисленного числа')
        await state.reset_state()
