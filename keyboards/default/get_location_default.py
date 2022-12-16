from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import _


async def location_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    send_location = KeyboardButton(text=_("🗺 Определить автоматически"), request_location=True)
    markup.add(send_location)
    return markup
