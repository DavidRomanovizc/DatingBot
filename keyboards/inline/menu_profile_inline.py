from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_profile_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    instagram = InlineKeyboardButton(text="📸 Instagram", callback_data="add_inst")
    turn_off = InlineKeyboardButton(text="❌ Удалить анкету", callback_data="disable")
    back = InlineKeyboardButton(text="⏪️ Назад", callback_data="back_to_sec_menu")
    markup.row(instagram, turn_off)
    markup.add(back)
    return markup
