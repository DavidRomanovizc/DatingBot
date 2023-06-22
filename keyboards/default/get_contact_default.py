from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _


async def contact_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text=_("📱 Отправить"), request_contact=True)
    markup.add(first_button)
    return markup
