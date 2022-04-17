from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def change_info_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    name = InlineKeyboardButton(text="Имя", callback_data="name")
    gender = InlineKeyboardButton(text="Пол", callback_data="gender")
    age = InlineKeyboardButton(text="Возраст", callback_data="age")
    city = InlineKeyboardButton(text="Город", callback_data="city")
    employment = InlineKeyboardButton(text="Занятость", callback_data="busyness")
    photo = InlineKeyboardButton(text="Фото", callback_data="photo")
    about_me = InlineKeyboardButton(text="О себе", callback_data="about_me")
    back_to_menu = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="second_m")
    markup.row(name, gender, age)
    markup.add(city)
    markup.row(employment, photo, about_me)
    markup.add(back_to_menu)
    return markup
