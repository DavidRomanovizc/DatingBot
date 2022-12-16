from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def registration_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    registration = InlineKeyboardButton(text=_("➕ Регистрация"), callback_data="registration")
    markup.add(registration)
    return markup


async def second_registration_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    questionnaire = InlineKeyboardButton(text=_("🖌️ Пройти опрос в боте"), callback_data="survey")
    back_to_menu = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="start_menu")
    markup.add(questionnaire, back_to_menu)
    return markup


async def confirm_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    yes_all_good = InlineKeyboardButton(text=_("✅ Да все хорошо!"), callback_data="yes_all_good")
    markup.add(yes_all_good)
    return markup


async def about_yourself_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    text = InlineKeyboardButton(text=_("💬 Текстом"), callback_data="send_text")
    voice = InlineKeyboardButton(text=_("🎤 Голосовым"), callback_data="send_voice")
    markup.add(text, voice)
    return markup
