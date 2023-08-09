from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def payments_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    settings = InlineKeyboardButton("⚙️ Настройки", callback_data="payments:settings")
    statistics = InlineKeyboardButton("📝 Статистика", callback_data="payments:stats")
    markup.add(statistics, settings)
    return markup
