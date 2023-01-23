from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


async def poster_keyboard(is_admin: bool, verification_status: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=6)
    create_poster = InlineKeyboardButton(text=_("✍️Создать афишу"), callback_data="create_poster")
    view_poster = InlineKeyboardButton(text=_("Смотреть афиши"), callback_data="view_poster")
    my_appointment = InlineKeyboardButton(text=_("📝 Мои записи"), callback_data="my_appointment")
    my_event = InlineKeyboardButton(text=_("🎭 Моё событие"), callback_data="my_event")
    back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="start_menu")
    if is_admin and verification_status:
        markup.add(my_event)
    markup.row(create_poster)
    markup.row(view_poster, my_appointment)
    markup.add(back)
    return markup


async def event_settings_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    change_data = InlineKeyboardButton(text=_("✍️ Изменить"), callback_data="change_event_data")
    back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="event_menu")
    markup.row(change_data)
    markup.add(back)
    return markup


async def change_datas_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    title = InlineKeyboardButton(text=_("Название"), callback_data="change_title")
    description = InlineKeyboardButton(text=_("Описание"), callback_data="change_description")
    back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="back_to_event_profile")
    markup.row(title, description)
    markup.add(back)
    return markup


async def create_moderate_ik(telegram_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    accept = InlineKeyboardButton(_("✅ Одобрить"), callback_data="moderate_accept-{}".format(telegram_id))
    reject = InlineKeyboardButton(_("❌ Отклонить"), callback_data="moderate_decline-{}".format(telegram_id))
    markup.row(accept, reject)
    return markup


async def view_event_keyboard(telegram_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    meet = InlineKeyboardButton(_("Пойду!"), callback_data="answer_imgoing-{}".format(telegram_id))
    not_interested = InlineKeyboardButton(_("Не интересно"),
                                          callback_data="answer_notinteresting-{}".format(telegram_id))
    stopped = InlineKeyboardButton(text=_("⏪️ Остановить"), callback_data="answer_stopped_view")
    markup.row(meet, not_interested)
    markup.add(stopped)
    return markup


async def cancel_event_keyboard(telegram_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    backed_out = InlineKeyboardButton(_("Дальше ⏩"), callback_data="cancel-{}".format(telegram_id))
    stopped = InlineKeyboardButton(_("⏪️ Остановить"), callback_data="go_out")
    markup.add(backed_out)
    markup.add(stopped)
    return markup


async def cancel_registration_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    stopped = InlineKeyboardButton(_("⏪️ Остановить"), callback_data="cancel_registration")
    markup.add(stopped)
    return markup
