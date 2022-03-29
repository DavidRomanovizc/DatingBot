from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gender_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    male = InlineKeyboardButton(text='Мужской', callback_data='male')
    female = InlineKeyboardButton(text='Женский', callback_data='female')
    markup.add(male, female)
    return markup


async def car_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    first_button = InlineKeyboardButton(text='Есть', callback_data='true')
    second_button = InlineKeyboardButton(text='Нет', callback_data='false')
    markup.add(first_button, second_button)
    return markup


async def kids_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    first_button = InlineKeyboardButton(text='Есть', callback_data='true')
    second_button = InlineKeyboardButton(text='Нет', callback_data='false')
    markup.add(first_button, second_button)
    return markup


async def house_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    first_button = InlineKeyboardButton(text='Есть', callback_data='true')
    second_button = InlineKeyboardButton(text='Нет', callback_data='false')
    markup.add(first_button, second_button)
    return markup


async def education_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    first_button = InlineKeyboardButton(text='Высшее', callback_data='higher_edu')
    second_button = InlineKeyboardButton(text='Среднее', callback_data='secondary_edu')
    markup.add(first_button, second_button)
    return markup
