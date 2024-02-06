from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


async def admin_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    customers = KeyboardButton("🫂 Пользователи")
    settings = KeyboardButton("⚙️ Настройки")
    advert = KeyboardButton("📊 Реклама")
    logs = KeyboardButton("🗒 Логи")
    monitoring = KeyboardButton(text="👀 Мониторинг")
    set_up_technical_works = KeyboardButton(text="🛑 Тех.Работа")
    markup.add(customers, monitoring)
    markup.add(settings)
    markup.add(logs, advert)
    markup.add(set_up_technical_works)
    return markup
