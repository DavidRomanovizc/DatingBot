from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


async def admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text=_("Рассылка"))
    btn2 = KeyboardButton(text=_("Сообщение по id"))
    btn3 = KeyboardButton(text=_("Посчитать людей и чаты"))
    btn4 = KeyboardButton(text=_("Мониторинг"))
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    return markup
