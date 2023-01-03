from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def change_info_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    name = InlineKeyboardButton(text=_("Имя"), callback_data="name")
    gender = InlineKeyboardButton(text=_("Пол"), callback_data="gender")
    age = InlineKeyboardButton(text=_("Возраст"), callback_data="age")
    city = InlineKeyboardButton(text=_("Город"), callback_data="city")
    photo = InlineKeyboardButton(text=_("Фото"), callback_data="photo")
    about_me = InlineKeyboardButton(text=_("О себе"), callback_data="about_me")
    back_to_menu = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="back_to_profile_menu")
    markup.row(name, gender, age)
    markup.row(city, photo, about_me)
    markup.add(back_to_menu)
    return markup


# TODO: Можно установить у функции параметр text, чтобы текст кнопки менялся в зависимости от задачи
async def gender_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    male = InlineKeyboardButton(text=_("Парень"), callback_data="male")
    female = InlineKeyboardButton(text=_("Девушка"), callback_data="female")
    markup.row(male, female)
    return markup
