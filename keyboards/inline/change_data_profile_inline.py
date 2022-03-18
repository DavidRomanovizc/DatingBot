from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def change_info_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    name = InlineKeyboardButton(text="Имя", callback_data="name")
    gender = InlineKeyboardButton(text="Пол", callback_data="gender")
    age = InlineKeyboardButton(text="Возраст", callback_data="age")
    nationality = InlineKeyboardButton(text="Национальность", callback_data="nationality")
    city = InlineKeyboardButton(text="Город", callback_data="city")
    education = InlineKeyboardButton(text="Образование", callback_data="education")
    car = InlineKeyboardButton(text="Машина", callback_data="car")
    housing = InlineKeyboardButton(text="Жилье", callback_data="house")
    employment = InlineKeyboardButton(text="Занятость", callback_data="busyness")
    kids = InlineKeyboardButton(text="Дети", callback_data="kids")
    photo = InlineKeyboardButton(text="Фото", callback_data="photo")
    about_me = InlineKeyboardButton(text="О себе", callback_data="about_me")
    back_to_menu = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="start_menu")
    markup.row(name, gender, age)
    markup.add(nationality)
    markup.row(city, housing, car)
    markup.add(education)
    markup.row(employment, kids, photo)
    markup.add(about_me)
    markup.add(back_to_menu)
    return markup
