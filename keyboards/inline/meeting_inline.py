from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def meeting_keyboard():
    markup = InlineKeyboardMarkup()
    create_ques = InlineKeyboardButton("Создать анкету", callback_data="create_ques")
    view_ques = InlineKeyboardButton("Смотреть анкеты", callback_data="view_ques")
    back_to_menu = InlineKeyboardButton("⏪️ Вернуться в меню", callback_data="second_m")
    markup.add(create_ques, view_ques)
    markup.add(back_to_menu)
    return markup


async def reaction_meetings_keyboard():
    markup = InlineKeyboardMarkup()
    further = InlineKeyboardButton("Далее", callback_data="further")
    back_to_menu = InlineKeyboardButton("⏪️ Вернуться в меню", callback_data="stopped")
    markup.add(further)
    markup.add(back_to_menu)
    return markup