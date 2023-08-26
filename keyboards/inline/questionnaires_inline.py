from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import _

action_keyboard = CallbackData("questionnaire", "action", "target_id")
action_keyboard_monitoring = CallbackData(
    "questionnaire_monitoring", "action", "target_id"
)
action_reciprocity_keyboard = CallbackData("questionnaire", "action", "user_for_like")
action_report_keyboard = CallbackData("report", "action", "target_id")


async def questionnaires_keyboard(
        target_id: int, monitoring: bool = False
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5)
    like = InlineKeyboardButton(
        text="❤️", callback_data=action_keyboard.new(action="like", target_id=target_id)
    )
    dislike = InlineKeyboardButton(
        text="👎",
        callback_data=action_keyboard.new(action="dislike", target_id=target_id),
    )
    report = InlineKeyboardButton(
        text="🔞",
        callback_data=action_keyboard.new(action="report", target_id=target_id),
    )
    go_back = InlineKeyboardButton(
        text=_("⏪️ Остановить"),
        callback_data=action_keyboard.new(action="stopped", target_id=target_id),
    )
    ban = InlineKeyboardButton(
        text=_("🚫 Забанить"),
        callback_data=action_keyboard_monitoring.new(action="ban", target_id=target_id),
    )
    next_btn = InlineKeyboardButton(
        text=_("Следующий"),
        callback_data=action_keyboard_monitoring.new(
            action="next", target_id=target_id
        ),
    )
    if not monitoring:
        markup.row(like, report, dislike)
        markup.add(go_back)
        return markup
    else:
        markup.row(ban)
        markup.row(next_btn)
        return markup


async def reciprocity_keyboard(user_for_like: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    like = InlineKeyboardButton(
        text="❤️",
        callback_data=action_reciprocity_keyboard.new(
            action="like_reciprocity", user_for_like=user_for_like
        ),
    )
    dislike = InlineKeyboardButton(
        text="👎",
        callback_data=action_reciprocity_keyboard.new(
            action="dislike_reciprocity", user_for_like=user_for_like
        ),
    )
    markup.row(like, dislike)

    return markup


async def viewing_ques_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    view_ques = InlineKeyboardButton(text=_("🚀 Смотреть"), callback_data="find_ques")
    markup.row(view_ques)
    return markup


async def user_link_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    open_chat = InlineKeyboardButton(
        text=_("👉 Перейти в чат"), url=f"tg://user?id={telegram_id}"
    )
    back = InlineKeyboardButton(
        text=_("⏪️ Вернуться к просмотру анкет"),
        callback_data="go_back_to_viewing_ques",
    )
    markup.add(open_chat, back)
    return markup


async def report_menu_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    adults_only = InlineKeyboardButton(
        text="🔞",
        callback_data=action_report_keyboard.new(
            action="adults_only", target_id=telegram_id
        ),
    )
    drugs = InlineKeyboardButton(
        text="💊",
        callback_data=action_report_keyboard.new(action="drugs", target_id=telegram_id),
    )
    scam = InlineKeyboardButton(
        text="💰",
        callback_data=action_report_keyboard.new(action="scam", target_id=telegram_id),
    )
    another = InlineKeyboardButton(
        text="🦨",
        callback_data=action_report_keyboard.new(
            action="another", target_id=telegram_id
        ),
    )
    cancel = InlineKeyboardButton(
        text="❌",
        callback_data=action_report_keyboard.new(
            action="cancel_report", target_id=telegram_id
        ),
    )
    markup.add(adults_only, drugs, scam, another, cancel)
    return markup
