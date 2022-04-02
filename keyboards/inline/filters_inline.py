from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

filters_data_kb = CallbackData("filter", "checker")


async def filters_keyboard():
    markup = InlineKeyboardMarkup(row_width=3)
    search_name = InlineKeyboardButton(text="Поиск по имени", callback_data=filters_data_kb.new(checker="name"))
    search_age = InlineKeyboardButton(text="Поиск по возрасту", callback_data=filters_data_kb.new(checker="age"))
    search_city = InlineKeyboardButton(text="Поиск по городу", callback_data=filters_data_kb.new(checker="city"))
    search_nationality = InlineKeyboardButton(text="Поиск по национальности",
                                              callback_data=filters_data_kb.new(checker="nationality"))
    back_to_menu = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="second_m")
    markup.row(search_name, search_age)
    markup.add(search_city)
    markup.row(search_nationality)
    markup.add(back_to_menu)
    return markup
