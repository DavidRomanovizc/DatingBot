from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def filters_keyboard():
    markup = InlineKeyboardMarkup()
    user_need_city = InlineKeyboardButton(text="🏙️ Город партнера", callback_data="needs_city")
    user_age_period = InlineKeyboardButton(text="🔞 Возр.диапазон", callback_data='user_age_period')
    user_need_gender = InlineKeyboardButton(text="🚻 Пол партнера", callback_data='user_need_gender')
    back = InlineKeyboardButton(text="⏪️ Назад", callback_data="back_with_delete")
    markup.add(user_need_city)
    markup.row(user_need_gender, user_age_period)
    markup.add(back)
    return markup
