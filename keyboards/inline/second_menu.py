from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def second_menu_keyboard():
    markup = InlineKeyboardMarkup(row_width=3)
    my_profile = InlineKeyboardButton(text="💬 Моя анекта", callback_data="my_profile")
    view_ques = InlineKeyboardButton(text="🧐 Смотреть анкеты", callback_data="find_ancets")
    edit_profile = InlineKeyboardButton(text="⬆️ Изменить анкету", callback_data="change_profile")
    back_to_menu = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="start_menu")
    verification = InlineKeyboardButton(text="✅ Верификация", callback_data="verification")
    balance = InlineKeyboardButton(text="💸 Баланс", callback_data="balance")
    markup.row(my_profile, verification)
    markup.add(balance)
    markup.row(view_ques, edit_profile)
    markup.add(back_to_menu)
    return markup
