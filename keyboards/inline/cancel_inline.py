from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


async def cancel_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    cancel = InlineKeyboardButton(text=_("Отмена"), callback_data="cancel")
    markup.add(cancel)
    return markup
