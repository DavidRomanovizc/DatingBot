from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def add_admins_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    add = InlineKeyboardButton("*️⃣ Добавить", callback_data="admin:admins:add")
    delete = InlineKeyboardButton("❌ Удалить", callback_data="admin:admins:delete")
    back = InlineKeyboardButton("◀️ Назад", callback_data="admin:settings")
    markup.add(add, delete)
    markup.add(back)
    return markup
