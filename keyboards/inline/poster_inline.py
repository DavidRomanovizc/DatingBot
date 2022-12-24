from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def poster_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    create_poster = InlineKeyboardButton(text=_("✍️Создать афишу"), callback_data="create_poster")
    view_poster = InlineKeyboardButton(text=_("📆 Смотреть афиши"), callback_data="view_poster")
    my_appointment = InlineKeyboardButton(text=_("📝 Мои записи"), callback_data="my_appointment")
    markup.row(create_poster, my_appointment)
    markup.add(view_poster)
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
