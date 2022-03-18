from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def registration_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    questionnaire = InlineKeyboardButton(text="Пройти опрос", callback_data="survey")
    back_to_menu = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="start_menu")
    markup.add(questionnaire, back_to_menu)
    return markup
