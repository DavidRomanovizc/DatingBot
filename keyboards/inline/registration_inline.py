from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def gender_keyboard():
    markup = InlineKeyboardMarkup(row_with=1)
    male = InlineKeyboardButton(text='Мужской', callback_data='male_reg')
    female = InlineKeyboardButton(text='Женский', callback_data='female_reg')
    markup.add(male, female)
    return markup


async def education_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    higher_edu = InlineKeyboardButton(text='Высшее', callback_data='higher_edu')
    secondary_edu = InlineKeyboardButton(text='Среднее', callback_data='secondary_edu')
    markup.add(higher_edu, secondary_edu)
    return markup


async def town_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    true = InlineKeyboardButton(text='Да', callback_data='car_true')
    false = InlineKeyboardButton(text='Нет', callback_data='car_false')
    markup.add(true, false)
    return markup


async def car_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    true = InlineKeyboardButton(text='Да', callback_data='apart_true')
    false = InlineKeyboardButton(text='Нет', callback_data='apart_false')
    markup.add(true, false)
    return markup


async def hobbies_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    busy = InlineKeyboardButton(text='Занят', callback_data='busy')
    not_busy = InlineKeyboardButton(text='Не занят', callback_data='not_busy')
    markup.add(busy, not_busy)
    return markup


async def family_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    true = InlineKeyboardButton(text='Да', callback_data='true')
    false = InlineKeyboardButton(text='Нет', callback_data='false')
    markup.add(true, false)
    return markup
