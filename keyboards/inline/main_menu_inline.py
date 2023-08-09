from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

from data.config import load_config
from loader import _
from utils.db_api import db_commands


async def start_keyboard(obj: Union[CallbackQuery, Message]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    user_db = await db_commands.select_user(telegram_id=obj.from_user.id)
    status = user_db["status"]
    registration = InlineKeyboardButton(text=_("➕ Регистрация"), callback_data="registration")
    language = InlineKeyboardButton(text=_("🌐 Язык"), callback_data="language_reg")
    my_profile = InlineKeyboardButton(text=_("👤 Моя анекта"), callback_data="my_profile")
    filters = InlineKeyboardButton(text=_("⚙️ Фильтры"), callback_data="filters")
    view_ques = InlineKeyboardButton(text=_("💌 Найти пару"), callback_data="find_ques")
    meetings = InlineKeyboardButton(text=_("🗓️ Афиша"), callback_data="meetings")
    support = InlineKeyboardButton(text=_("🆘 Поддержка"), callback_data="support")
    information = InlineKeyboardButton(text=_("ℹ️ Информация"), callback_data="information")
    if not status:
        markup.row(registration)
        markup.row(support, information)
        markup.row(language)
    else:
        markup.row(my_profile)
        markup.row(view_ques, meetings)
        markup.row(information, filters)
        if load_config().tg_bot.support_ids[0] != obj.from_user.id:
            markup.row(support)
    return markup
