from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


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
