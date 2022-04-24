from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    registration = InlineKeyboardButton(text="➕ Регистрация", callback_data="registration")
    menu_of_bot = InlineKeyboardButton(text="📚 Меню бота", callback_data="second_m")
    view_ques = InlineKeyboardButton(text="💌 Найти пару", callback_data="find_ancets")
    information = InlineKeyboardButton(text="🌐 Руководство", callback_data="info")
    statistics = InlineKeyboardButton(text="📈 Статистика", callback_data="statistics")
    support = InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")
    markup.row(registration, menu_of_bot)
    markup.add(view_ques)
    markup.row(information, statistics)
    markup.add(support)
    return markup
