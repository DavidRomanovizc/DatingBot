from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    registration = InlineKeyboardButton(text="➕ Регистрация", callback_data="registration")
    menu_of_bot = InlineKeyboardButton(text="📚 Меню бота", callback_data="second_m")
    information = InlineKeyboardButton(text="🌐 Информация", callback_data="info")
    balance = InlineKeyboardButton(text="💎 Премиум", callback_data="premium")
    statistics = InlineKeyboardButton(text="📈 Статистика", callback_data="statistics")
    support = InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")
    markup.row(registration, menu_of_bot)
    markup.add(information)
    markup.row(balance, statistics)
    markup.add(support)
    return markup
