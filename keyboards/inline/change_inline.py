from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gender_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    male = InlineKeyboardButton(text='Мужской', callback_data='male')
    female = InlineKeyboardButton(text='Женский', callback_data='female')
    markup.add(male, female)
    return markup
