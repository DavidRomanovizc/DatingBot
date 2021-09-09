from os import terminal_size
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class MarupDatas:  # Это не удалять, нужная штука
    ALL_INFO = {
        "Имя : ": "name",
        "Возраст : ": "age",
        "Национальность : ": "nationality",
        "Образование : ": "education",
        "Город : ": "town",
        "Машина : ": "car",
        "Жилье : ": "own_home",
        "Занятие : ": "hobbies",
        "Дети : ": "child",
        "Семейное положение : ": "marital"
    }


change_Keyboard = InlineKeyboardMarkup()
