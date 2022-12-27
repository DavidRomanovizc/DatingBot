from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def poster_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=6)
    create_poster = InlineKeyboardButton(text=_("✍️Создать афишу"), callback_data="create_poster")
    view_poster = InlineKeyboardButton(text=_("Смотреть афиши"), callback_data="view_poster")
    my_appointment = InlineKeyboardButton(text=_("📝 Мои записи"), callback_data="my_appointment")
    my_event = InlineKeyboardButton(text=_("🎭 Моё событие"), callback_data="my_event")
    event_filters = InlineKeyboardButton(text=_("⚙️ Фильтры"), callback_data="event_filters")
    back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="start_menu")
    if is_admin:
        markup.add(my_event)
    markup.row(create_poster, event_filters)
    markup.row(view_poster, my_appointment)
    markup.add(back)
    return markup


async def event_filters_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    city_event = InlineKeyboardButton(text=_("Город"), callback_data="city_event")
    cost_of_event = InlineKeyboardButton(text=_("Стоимость"), callback_data="cost_of_event")
    event_category = InlineKeyboardButton(text=_("Категории"), callback_data="event_category")
    back = InlineKeyboardButton(text=_("⏪️ Вернуться в меню"), callback_data="event_menu")
    markup.add(city_event)
    markup.row(cost_of_event, event_category)
    markup.add(back)
    return markup


async def create_moderate_ik(telegram_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    accept = InlineKeyboardButton(_("✅ Одобрить"), callback_data="moderate_accept-{}".format(telegram_id))
    reject = InlineKeyboardButton(_("❌ Отклонить"), callback_data="moderate_decline-{}".format(telegram_id))
    markup.row(accept, reject)
    return markup


async def create_event_list_ik(telegram_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    meet = InlineKeyboardButton(_("Пойду!"), callback_data="answer_imgoing-{}".format(telegram_id))
    not_interested = InlineKeyboardButton(_("Не интересно"),
                                          callback_data="answer_notinteresting-{}".format(telegram_id))
    markup.row(meet, not_interested)
    return markup


async def cancel_event_list_ik(telegram_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    backed_out = InlineKeyboardButton(_("Отказаться от участия!"), callback_data="cancel-{}".format(telegram_id))
    markup.add(backed_out)
    return markup
