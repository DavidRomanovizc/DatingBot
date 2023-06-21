from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import _

action_keyboard = CallbackData("questionnaire", "action", "target_id")
action_keyboard_monitoring = CallbackData("questionnaire_monitoring", "action", "target_id")
action_reciprocity_keyboard = CallbackData("questionnaire", "action", "user_for_like")


# TODO: Добавить кнопки: подарок и отправка сообщений

async def questionnaires_keyboard(target_id, monitoring=False, report_system=False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5)
    like = InlineKeyboardButton(text='❤️', callback_data=action_keyboard.new(action="like",
                                                                             target_id=target_id))
    dislike = InlineKeyboardButton(text='👎', callback_data=action_keyboard.new(action="dislike",
                                                                                target_id=1))
    go_back = InlineKeyboardButton(text=_("⏪️ Остановить"),
                                   callback_data=action_keyboard.new(action="stopped",
                                                                     target_id=1))
    ban = InlineKeyboardButton(text=_("🚫 Забанить"),
                               callback_data=action_keyboard_monitoring.new(action="ban",
                                                                            target_id=target_id))
    next_btn = InlineKeyboardButton(text=_("Следующий"), callback_data=action_keyboard_monitoring.new(action="next",
                                                                                                      target_id=1))
    if not monitoring and not report_system:
        markup.row(like, dislike)
        markup.add(go_back)
        return markup
    elif report_system:
        markup.row(ban)
        return markup
    else:
        markup.row(ban)
        markup.row(next_btn)
        return markup


async def reciprocity_keyboard(user_for_like) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    like = InlineKeyboardButton(text='❤️', callback_data=action_reciprocity_keyboard.new(action="like_reciprocity",
                                                                                         user_for_like=user_for_like))
    dislike = InlineKeyboardButton(text='👎',
                                   callback_data=action_reciprocity_keyboard.new(action="dislike_reciprocity",
                                                                                 user_for_like=1))
    markup.row(like, dislike)

    return markup


async def back_viewing_ques_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton(text=_("Вернуться к просмотру анкет"), callback_data="go_back_to_viewing_ques")
    markup.row(back)

    return markup


async def viewing_ques_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    view_ques = InlineKeyboardButton(text=_("🚀 Смотреть"), callback_data="find_ques")
    markup.row(view_ques)
    return markup
