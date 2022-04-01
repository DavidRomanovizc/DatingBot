from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def registration_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    registration = InlineKeyboardButton(text="➕ Регистрация", callback_data="registration")
    markup.add(registration)
    return markup