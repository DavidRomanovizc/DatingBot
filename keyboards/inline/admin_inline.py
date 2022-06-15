from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def add_buttons_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="Подтвердить отправку", callback_data="confirm_send")
    btn2 = InlineKeyboardButton(text="Добавить кнопку", callback_data="add_buttons")
    btn3 = InlineKeyboardButton(text="Отмена", callback_data="cancel")

    markup.add(btn1, btn2, btn3)
    return markup


async def confirm_with_button_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="Подтвердить отправку", callback_data="confirm_send_with_button")
    btn2 = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    markup.add(btn1, btn2)
    return markup


async def start_monitoring_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="Подтвердить отправку", callback_data="confirm_send_monitoring")
    markup.add(btn1)
    return markup
