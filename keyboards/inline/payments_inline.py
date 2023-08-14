from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yarl import URL

from loader import _


async def payments_keyboard(url: str | URL = None) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    pay_qiwi = InlineKeyboardButton(text=_("💳 ЮMoney"), url=url)
    check_prices = InlineKeyboardButton(text=_("🔄 Проверить оплату"), callback_data="check_payment")
    markup.add(pay_qiwi, check_prices)
    return markup
