from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def cancel_keyboard():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    markup.add(btn1)
    return markup
