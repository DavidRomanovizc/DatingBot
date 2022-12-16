from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def sponsors_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    sponsor = InlineKeyboardButton(_("🕴️ Спонсорство"), callback_data="sponsors")
    back_to_menu = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="start_menu")
    markup.add(sponsor)
    markup.add(back_to_menu)
    return markup


async def sponsor_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    donate = InlineKeyboardButton(text=_("💰 Донат"), url="https://www.donationalerts.com/r/quegroup")
    back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="statistics")
    markup.add(donate)
    markup.add(back)
    return markup
