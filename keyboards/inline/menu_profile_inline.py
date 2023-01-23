from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


async def get_profile_keyboard(verification) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    if not verification:
        verification_btn = InlineKeyboardButton(text=_("✅ Верификация"), callback_data="verification")
        markup.row(verification_btn)
    edit_profile = InlineKeyboardButton(text=_("Изменить анкету"), callback_data="change_profile")
    language = InlineKeyboardButton(text=_("🌐 Язык"), callback_data="language")
    instagram = InlineKeyboardButton(text=_("📸 Instagram"), callback_data="add_inst")
    turn_off = InlineKeyboardButton(text=_("Удалить анкету"), callback_data="disable")
    back = InlineKeyboardButton(text=_("⏪ Назад"), callback_data="back_with_delete")
    markup.row(language, instagram)
    markup.add(edit_profile, turn_off)
    markup.add(back)
    return markup
