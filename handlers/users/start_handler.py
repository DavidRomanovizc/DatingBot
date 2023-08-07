import aiogram
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import BadRequest

from data.config import load_config
from filters import IsPrivate
from functions.main_app.auxiliary_tools import registration_menu
from handlers.users.back import delete_message
from keyboards.inline.language_inline import language_keyboard
from loader import dp, _, bot
from utils.db_api import db_commands
from utils.db_api.db_commands import check_user_exists, check_user_meetings_exists


@dp.message_handler(IsPrivate(), CommandStart())
async def register_user(message: types.Message) -> None:
    username = message.from_user.username if message.from_user.username else ""
    telegram_id = message.from_user.id
    if not await check_user_exists(telegram_id) and not await check_user_meetings_exists(telegram_id):

        referrer_id = message.text[7:]
        if referrer_id != "" and referrer_id != telegram_id:
            await db_commands.add_user(
                name=message.from_user.full_name,
                telegram_id=telegram_id,
                username=username,
                referrer_id=referrer_id
            )
            await bot.send_message(chat_id=referrer_id,
                                   text="По вашей ссылке зарегистрировался пользователь {}!".format(
                                       message.from_user.username))
        else:
            await db_commands.add_user(
                name=message.from_user.full_name,
                telegram_id=telegram_id,
                username=username
            )
        await db_commands.add_meetings_user(telegram_id=telegram_id,
                                            username=username)
        if telegram_id in load_config().tg_bot.admin_ids:
            await db_commands.add_user_to_settings(telegram_id=telegram_id)
    await registration_menu(message)


@dp.callback_query_handler(text="start_menu")
async def start_menu(call: CallbackQuery) -> None:
    try:
        await registration_menu(call)
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
    "language_info": "information",
}


def register_callbacks(callback_dict, callback_function):
    for callback_text, value in callback_dict.items():
        dp.callback_query_handler(text=callback_text)(lambda call, value=value: callback_function(call, value))


register_callbacks(language_codes, change_language)
register_callbacks(language_menus, choice_language)
