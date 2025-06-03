from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from loader import (
    _,
)


async def get_profile_keyboard(verification) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    if not verification:
        verification_btn = InlineKeyboardButton(
            text=_("✅ Верификация"), callback_data="verification"
        )
        markup.row(verification_btn)
    edit_profile = InlineKeyboardButton(
        text=_("🖊️ Изменить"), callback_data="change_profile"
    )
    turn_off = InlineKeyboardButton(text=_("🗑️ Удалить"), callback_data="disable")
    back = InlineKeyboardButton(text=_("⏪ Назад"), callback_data="back_with_delete")
    markup.row(edit_profile, turn_off)
    markup.add(back)
    return markup
