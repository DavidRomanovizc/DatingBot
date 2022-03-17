from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def sex_partner():
    markup = InlineKeyboardMarkup(row_width=2)
    male = InlineKeyboardButton(text='Мужчин', callback_data='gen_male')
    female = InlineKeyboardButton(text='Женщин', callback_data='g_fe')
    markup.row(male, female)
    return markup
