from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


async def first_str_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    forward = InlineKeyboardButton(text=_("Вперед ➡️"), callback_data='forward_f')
    back = InlineKeyboardButton(text=_("❌ Закрыть"), callback_data='back_with_delete')
    markup.add(forward)
    markup.add(back)
    return markup


async def second_str_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    backward = InlineKeyboardButton(text=_("⏪️ Назад"), callback_data='backward_s')
    forward = InlineKeyboardButton(text=_("Вперед ➡️"), callback_data='forward_s')
    back = InlineKeyboardButton(text=_("❌ Закрыть"), callback_data='back_with_delete')
    markup.add(backward, forward)
    markup.add(back)
    return markup


async def third_str_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    backward = InlineKeyboardButton(text=_("⏪️ Назад"), callback_data='backward_th')
    forward = InlineKeyboardButton(text=_("Вперед ➡️"), callback_data='forward_th')
    back = InlineKeyboardButton(text=_("❌ Закрыть"), callback_data='back_with_delete')
    markup.add(backward, forward)
    markup.add(back)
    return markup


async def fourth_str_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    backward = InlineKeyboardButton(text=_("⏪️ Назад"), callback_data='backward_four')
    back = InlineKeyboardButton(text=_("❌ Закрыть"), callback_data='back_with_delete')
    markup.add(backward)
    markup.add(back)
    return markup
