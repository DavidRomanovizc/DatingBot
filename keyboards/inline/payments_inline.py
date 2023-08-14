from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yarl import URL

from loader import _


async def payments_keyboard(menu: str, url: str | URL = None) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    pay_qiwi = InlineKeyboardButton(text=_("💳 ЮMoney"), url=url)
    check_prices = InlineKeyboardButton(text=_("🔄 Проверить цены"), callback_data="check_price")
    markup.add(pay_qiwi, check_prices)
    if menu == "unban":
        back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="unban_menu")
        markup.add(back)
    else:
        back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="start_menu")
        markup.add(back)
    return markup


async def making_payment(bill) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    settle_bill = InlineKeyboardButton(text=_("Оплатить"), url=bill.pay_url)
    check_payment = InlineKeyboardButton(text=_("Проверить оплату"), callback_data='check_payment')
    cancel = InlineKeyboardButton(text=_("Отмена"), callback_data='cancel_payment')
    markup.add(settle_bill)
    markup.add(check_payment)
    markup.add(cancel)
    return markup


async def check_payment_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    check_payment = InlineKeyboardButton(text=_("Проверить оплату"), callback_data='check_payment')
    markup.add(check_payment)
    return markup
