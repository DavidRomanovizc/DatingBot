from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def sponsors_keyboard():
    markup = InlineKeyboardMarkup()
    sponsor = InlineKeyboardButton("🕴️ Спонсорство", callback_data="sponsors")
    back_to_menu = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="start_menu")
    markup.add(sponsor)
    markup.add(back_to_menu)
    return markup



async def sponsor_keyboard():
    markup = InlineKeyboardMarkup()
    donate = InlineKeyboardButton("💰 Донат", url="https://www.donationalerts.com/r/quegroup")
    back = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="statistics")
    markup.add(donate)
    markup.add(back)
    return markup