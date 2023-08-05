import random

import aiogram
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import BadRequest
from django.db import IntegrityError

from data.config import load_config
from filters import IsPrivate
from functions.main_app.app_scheduler import send_message_week
from functions.main_app.auxiliary_tools import registration_menu
from handlers.users.back import delete_message
from keyboards.inline.language_inline import language_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp, scheduler, _, bot
from utils.db_api import db_commands


@dp.message_handler(IsPrivate(), CommandStart())
async def register_user(message: types.Message) -> None:
    try:
        referrer_id = message.text[7:]
        if referrer_id != "" and referrer_id != message.from_user.id:
            await db_commands.add_user(
                name=message.from_user.full_name,
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                referrer_id=referrer_id
            )
            await bot.send_message(chat_id=referrer_id,
                                   text="По вашей ссылке зарегистрировался пользователь {}!".format(
                                       message.from_user.username))
        else:
            await db_commands.add_user(
                name=message.from_user.full_name,
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
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
        markup = await start_keyboard(message)
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
        await registration_menu(call, scheduler, send_message_week)
    except TypeError:
        await call.message.answer(_("Вас нет в базе данной"))


async def choice_language(call: CallbackQuery, menu: str) -> None:
    try:
        await call.message.edit_text(_("Выберите язык"), reply_markup=await language_keyboard(menu))
    except BadRequest:
        await delete_message(call.message)
        await call.message.answer(_("Выберите язык"), reply_markup=await language_keyboard(menu))


async def change_language(call: CallbackQuery, language: str) -> None:
    telegram_id = call.from_user.id
    try:
        await db_commands.update_user_data(telegram_id=telegram_id, language=language)
        await call.message.edit_text(_("Язык был успешно изменен. Введите команду /start", locale=language))
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        await call.message.edit_text(_("Произошла какая-то ошибка. Введите команду /start и попробуйте еще раз"))


language_codes = {
    "Russian": "ru",
    "Deutsch": "de",
    "English": "en",
    "Indonesian": "id",
}

language_menus = {
    "language_reg": "registration",
    "language": "profile",
    "language_info": "information",
}


def register_callbacks(callback_dict, callback_function):
    for callback_text, value in callback_dict.items():
        dp.callback_query_handler(text=callback_text)(lambda call, value=value: callback_function(call, value))


register_callbacks(language_codes, change_language)
register_callbacks(language_menus, choice_language)
