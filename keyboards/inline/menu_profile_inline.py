from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_profile():
    markup = InlineKeyboardMarkup()
    turn_off = InlineKeyboardButton(text="Отключить анкету", callback_data="disable")
    back = InlineKeyboardButton(text="Назад", callback_data="back_to_sec_menu")
    markup.add(turn_off)
    markup.add(back)
    return markup
