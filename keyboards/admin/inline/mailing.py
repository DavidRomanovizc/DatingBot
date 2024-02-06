from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from loader import (
    _,
)


async def mailing_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    mailing = InlineKeyboardButton(_("📧 Рассылка"), callback_data="adv:mailing")
    markup.add(mailing)
    return markup


async def add_buttons_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    confirm_sending = InlineKeyboardButton(
        text=_("Подтвердить отправку"), callback_data="confirm_send"
    )
    add_button = InlineKeyboardButton(
        text=_("Добавить кнопку"), callback_data="add_buttons"
    )
    cancel = InlineKeyboardButton(text=_("Отмена"), callback_data="cancel")

    markup.row(confirm_sending, add_button)
    markup.add(cancel)
    return markup


async def confirm_with_button_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    confirm_sending = InlineKeyboardButton(
        text=_("Подтвердить отправку"), callback_data="confirm_send_with_button"
    )
    cancel = InlineKeyboardButton(text=_("Отмена"), callback_data="cancel")
    markup.add(confirm_sending)
    markup.add(cancel)
    return markup
