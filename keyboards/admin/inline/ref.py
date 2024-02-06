from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from loader import (
    _,
)


async def referral_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    statistics = InlineKeyboardButton(_("📈 Статистика"), callback_data="ref_urls:stats")
    add_ref = InlineKeyboardButton(_("*️⃣ Добавить"), callback_data="ref_urls:create")
    delete_ref = InlineKeyboardButton(_("❌ Удалить"), callback_data="ref_urls:delete")
    back = InlineKeyboardButton(_("◀️ Назад"), callback_data="admin:mailing_md")
    markup.add(statistics, add_ref, delete_ref, back)
    return markup
