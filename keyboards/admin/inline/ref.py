from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def referral_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    statistics = InlineKeyboardButton("📈 Статистика", callback_data="ref_urls:stats")
    add_ref = InlineKeyboardButton("*️⃣ Добавить", callback_data="ref_urls:create")
    delete_ref = InlineKeyboardButton("❌ Удалить", callback_data="ref_urls:delete")
    back = InlineKeyboardButton("◀️ Назад", callback_data="admin:mailing_md")
    markup.add(statistics, add_ref, delete_ref, back)
    return markup
