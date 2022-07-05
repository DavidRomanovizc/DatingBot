from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_keyboard(status):
    markup = InlineKeyboardMarkup(row_width=2)
    if not status:
        registration = InlineKeyboardButton(text="➕ РЕГИСТРАЦИЯ", callback_data="registration")
        information = InlineKeyboardButton(text="🌐 Руководство", callback_data="info")
        support = InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")
        markup.row(registration)
        markup.row(support, information)
        return markup
    else:
        my_profile = InlineKeyboardButton(text="👤 Моя анекта", callback_data="my_profile")
        filters = InlineKeyboardButton(text="⚙️ Фильтры", callback_data="filters")
        view_ques = InlineKeyboardButton(text="💌 Найти пару", callback_data="find_ancets")
        meetings = InlineKeyboardButton(text="💎 Тусовки", callback_data="meetings")
        information = InlineKeyboardButton(text="🌐 Руководство", callback_data="info")
        statistics = InlineKeyboardButton(text="📈 Статистика", callback_data="statistics")
        support = InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")
        markup.row(my_profile, filters)
        markup.row(view_ques, meetings)
        markup.row(information, statistics)
        markup.add(support)
        return markup
