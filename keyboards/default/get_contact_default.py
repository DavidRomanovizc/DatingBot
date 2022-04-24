from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def contact_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text='📱 Отправить', request_contact=True)
    markup.add(first_button)
    return markup
