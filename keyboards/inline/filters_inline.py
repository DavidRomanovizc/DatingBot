from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def filters_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    user_need_city = InlineKeyboardButton(text=_("🏙️ Город партнера"), callback_data="needs_city")
    user_age_period = InlineKeyboardButton(text=_("🔞 Возр.диапазон"), callback_data='user_age_period')
    user_need_gender = InlineKeyboardButton(text=_("🚻 Пол партнера"), callback_data='user_need_gender')
    back = InlineKeyboardButton(text=_("⏪️ Назад"), callback_data="back_with_delete")
    markup.add(user_need_city)
    markup.row(user_need_gender, user_age_period)
    markup.add(back)
    return markup
