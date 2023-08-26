from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


async def payments_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    settings = InlineKeyboardButton(
        _("⚙️ Настройки"), callback_data="payments:settings"
    )
    statistics = InlineKeyboardButton(_("📝 Статистика"), callback_data="payments:stats")
    markup.add(statistics, settings)
    return markup
