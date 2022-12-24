from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def start_keyboard(status) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    if not status:
        registration = InlineKeyboardButton(text=_("➕ Регистрация"), callback_data="registration")
        information = InlineKeyboardButton(text=_("💬 Руководство"), callback_data="info")
        support = InlineKeyboardButton(text=_("🆘 Поддержка"), callback_data="support")
        language = InlineKeyboardButton(text=_("🌐 Язык"), callback_data="language")
        markup.row(registration)
        markup.row(support, information)
        markup.row(language)
        return markup
    else:
        my_profile = InlineKeyboardButton(text=_("👤 Моя анекта"), callback_data="my_profile")
        filters = InlineKeyboardButton(text=_("⚙️ Фильтры"), callback_data="filters")
        view_ques = InlineKeyboardButton(text=_("💌 Найти пару"), callback_data="find_ques")
        meetings = InlineKeyboardButton(text=_("🗓️ Афиша"), callback_data="meetings")
        information = InlineKeyboardButton(text=_("💬 Руководство"), callback_data="info")
        statistics = InlineKeyboardButton(text=_("📈 Статистика"), callback_data="statistics")
        support = InlineKeyboardButton(text=_("🆘 Поддержка"), callback_data="support")
        markup.row(my_profile, filters)
        markup.row(view_ques, meetings)
        markup.row(information, statistics)
        markup.add(support)
        return markup
