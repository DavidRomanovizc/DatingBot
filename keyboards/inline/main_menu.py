from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    registration = InlineKeyboardButton(text="➕ Регистрация", callback_data="registration")
    menu_of_bot = InlineKeyboardButton(text="📄 Меню бота", callback_data="second_m")
    information = InlineKeyboardButton(text="🌐 Информация", callback_data="info")
    sponsor = InlineKeyboardButton(text="💚 Спонсорство", url="https://www.donationalerts.com/r/david_romanov")
    statistics = InlineKeyboardButton(text="📈 Статистика", callback_data="statistics")
    markup.row(registration, menu_of_bot)
    markup.add(information)
    markup.row(sponsor, statistics)
    return markup
