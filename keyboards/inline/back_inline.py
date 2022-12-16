from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def only_back_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="start_menu")
    markup.add(back)
    return markup
