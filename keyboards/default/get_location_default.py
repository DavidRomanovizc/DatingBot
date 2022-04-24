from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def location_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    send_location = KeyboardButton(text=f'🗺 Определить автоматически', request_location=True)
    markup.add(send_location)
    return markup
