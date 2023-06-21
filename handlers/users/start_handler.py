import asyncio
import random

import aiogram
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import BadRequest
from django.db import IntegrityError
from loguru import logger

from data.config import load_config
from filters import IsPrivate
from functions.main_app.app_scheduler import send_message_week
from functions.main_app.auxiliary_tools import registration_menu
from handlers.users.back_handler import delete_message
from keyboards.inline.language_inline import language_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp, scheduler, _
from utils.db_api import db_commands


@dp.message_handler(IsPrivate(), CommandStart())
async def register_user(message: types.Message) -> None:
    try:
        await db_commands.add_user(name=message.from_user.full_name,
                                   telegram_id=message.from_user.id,
                                   username=message.from_user.username)
        await db_commands.add_meetings_user(telegram_id=message.from_user.id,
                                            username=message.from_user.username)
        if message.from_user.id in load_config().tg_bot.admin_ids:
            await db_commands.add_user_to_settings(telegram_id=message.from_user.id)
    except IntegrityError as ex:
        err = str(ex).split()
        if err[0:2] == ['null', 'value']:
            await message.answer(_(
                "У вас не установлен username, пожалуйста,"
                " зайдите в настройки аккаунта и создайте username.\n"
                "<b>Без него вы не сможете пользоваться ботом</b>\n\n"
                '<a href="{url1}">Инструкция №1</a>\n'
                '<a href="{url2}">Инструкция №2</a>').format(
                url1="https://www.youtube.com/watch?v=6fC_AUJemSo&ab_channel=TheTechnology",
                url2="https://www.youtube.com/watch?v=xc9K2NjvfLo&ab_channel=AlexTrack"
            ))
        elif err[0:2] == ['duplicate', 'key']:
            pass
    try:
        support = await db_commands.select_user(telegram_id=load_config().tg_bot.support_ids[0])
        user_db = await db_commands.select_user(telegram_id=message.from_user.id)
        markup = await start_keyboard(status=user_db["status"])
        fullname = message.from_user.full_name

        heart = random.choice(['💙', '💚', '💛', '🧡', '💜', '🖤', '❤', '🤍', '💖', '💝'])
        await message.answer(_("Приветствую вас, {fullname}!!\n\n"
                               "{heart} <b> QueDateBot </b> - платформа для поиска новых знакомств.\n\n"
                               "🪧 Новости о проекте вы можете прочитать в нашем канале - "
                               "https://t.me/QueDateGroup \n\n"
                               "<b>🤝 Сотрудничество: </b>\n"
                               "Если у вас есть предложение о сотрудничестве, пишите агенту поддержки - "
                               "@{supports}\n\n").format(fullname=fullname, heart=heart,
                                                         supports=support['username']),
                             reply_markup=markup)
    except TypeError:
        pass


@dp.callback_query_handler(text="start_menu")
async def start_menu(call: CallbackQuery) -> None:
    try:
        await registration_menu(call, scheduler, send_message_week, load_config, random)
    except TypeError:
        await call.message.answer(_("Вас нет в базе данной"))


@dp.callback_query_handler(text="language")
@dp.callback_query_handler(text="language_reg")
async def choice_language(call: CallbackQuery) -> None:
    if call.data == "language_reg":
        try:
            await call.message.edit_text(_("Выберите язык"), reply_markup=await language_keyboard("registration"))
        except BadRequest:
            await delete_message(call.message)
            await call.message.answer(_("Выберите язык"), reply_markup=await language_keyboard("registration"))
    elif call.data == "language":
        try:
            await call.message.edit_text(_("Выберите язык"), reply_markup=await language_keyboard("profile"))
        except BadRequest:
            await delete_message(call.message)
            await call.message.answer(_("Выберите язык"), reply_markup=await language_keyboard("profile"))


@dp.callback_query_handler(text="Russian")
@dp.callback_query_handler(text="Deutsch")
@dp.callback_query_handler(text="English")
@dp.callback_query_handler(text="Indonesian")
async def change_language(call: CallbackQuery) -> None:
    telegram_id = call.from_user.id
    try:
        if call.data == "Russian":
            await db_commands.update_user_data(telegram_id=telegram_id, language="ru")
        elif call.data == "Deutsch":
            await db_commands.update_user_data(telegram_id=telegram_id, language="de")
        elif call.data == "English":
            await db_commands.update_user_data(telegram_id=telegram_id, language="en")
        elif call.data == "Indonesian":
            await db_commands.update_user_data(telegram_id=telegram_id, language="in")
        await call.answer(_("Язык был успешно изменен. Введите команду /start"), show_alert=True)
        await asyncio.sleep(5)
        await call.message.delete()
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        await call.message.answer(_("Произошла какая-то ошибка. Введите команду /start и попробуйте еще раз"))
