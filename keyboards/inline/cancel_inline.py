from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def cancel_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=_("Отмена"), callback_data="cancel")
    markup.add(btn1)
    return markup
