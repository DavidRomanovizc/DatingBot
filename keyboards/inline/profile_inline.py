from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def registration_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    questionnaire = InlineKeyboardButton(text="Пройти опрос в боте", callback_data="survey")
    web_questionnaire = InlineKeyboardButton(text="Пройти опрос на сайте", url="https://t.me")
    back_to_menu = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="start_menu")
    markup.add(questionnaire, web_questionnaire, back_to_menu)
    return markup
