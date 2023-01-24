from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


async def add_buttons_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    confirm_sending = InlineKeyboardButton(text=_("Подтвердить отправку"), callback_data="confirm_send")
    add_button = InlineKeyboardButton(text=_("Добавить кнопку"), callback_data="add_buttons")
    cancel = InlineKeyboardButton(text=_("Отмена"), callback_data="cancel")

    markup.row(confirm_sending, add_button)
    markup.add(cancel)
    return markup


async def confirm_with_button_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    confirm_sending = InlineKeyboardButton(text=_("Подтвердить отправку"), callback_data="confirm_send_with_button")
    cancel = InlineKeyboardButton(text=_("Отмена"), callback_data="cancel")
    markup.add(confirm_sending)
    markup.add(cancel)
    return markup


async def start_monitoring_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    confirm_sending = InlineKeyboardButton(text=_("Подтвердить отправку"), callback_data="confirm_send_monitoring")
    markup.add(confirm_sending)
    return markup


async def tech_works_keyboard(tech_works: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    set_up_tech_work = InlineKeyboardButton(text=_("Включить"), callback_data="set_up_tech_work")
    disable_technical_work = InlineKeyboardButton(text=_("Выключить"), callback_data="disable_tech_work")
    if tech_works:
        markup.add(disable_technical_work)
        return markup
    else:
        markup.add(set_up_tech_work)
        return markup


async def unban_user_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    unban_button = InlineKeyboardButton(_("Разблокировать"), callback_data="unban")
    markup.add(unban_button)
    return markup
