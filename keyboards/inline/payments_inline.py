from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def payments_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    pay_qiwi = InlineKeyboardButton(text=_("💳 Qiwi"), callback_data="pay_qiwi")
    check_prices = InlineKeyboardButton(text=_("🔄 Проверить цены"), callback_data="check_price")
    back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="start_menu")
    markup.add(pay_qiwi, check_prices)
    markup.add(back)
    return markup
