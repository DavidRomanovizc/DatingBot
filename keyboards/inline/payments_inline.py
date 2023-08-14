from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yarl import URL

from loader import _


async def payment_menu_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    yoomoney = InlineKeyboardButton(text=_("💳 ЮMoney"), callback_data="yoomoney")
    markup.add(yoomoney)
    return markup


async def yoomoney_keyboard(url: str | URL = None) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    pay_yoomoney = InlineKeyboardButton(text=_("💳 Оплатить"), url=url)
    check_prices = InlineKeyboardButton(text=_("🔄 Проверить оплату"), callback_data="yoomoney:check_payment")
    markup.add(pay_yoomoney, check_prices)
    return markup
