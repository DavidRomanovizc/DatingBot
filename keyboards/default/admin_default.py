from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text="Рассылка")
    btn2 = KeyboardButton(text="Сообщение по id")
    btn3 = KeyboardButton(text="Посчитать людей и чаты")
    btn4 = KeyboardButton(text="Мониторинг")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    return markup
