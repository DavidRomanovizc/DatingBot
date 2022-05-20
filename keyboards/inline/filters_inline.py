from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def filters_keyboard():
    markup = InlineKeyboardMarkup()
    user_age_period = InlineKeyboardButton(text="🔞 Возр.диапазон", callback_data='user_age_period')
    get_more_cod = InlineKeyboardButton(text="🌐 Город", callback_data='user_max_range')
    back = InlineKeyboardButton(text="⏪️ Назад", callback_data="back_to_sec_menu")
    markup.row(get_more_cod, user_age_period)
    markup.add(back)
    return markup
