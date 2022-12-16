import random
from loader import _
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.config import load_config
from keyboards.inline.support_inline import get_support_manager

moderate_callback = CallbackData("ask_support", "messages", "user_id", "as_user")
cancel_moderate_callback = CallbackData("cancel_support", "user_id")


async def moderate_keyboard(messages, user_id=None):
    if user_id:
        contact_id = int(user_id)
        as_user = "no"
        text = _("Одобрить")

    else:
        contact_id = await get_support_manager()
        as_user = "yes"
        if messages == "many" and contact_id is None:
            return False
        elif messages == "one" and contact_id is None:
            contact_id = random.choice(load_config().tg_bot.support_ids)

        text = _("Отправить форму")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=moderate_callback.new(
                messages=messages,
                user_id=contact_id,
                as_user=as_user
            )
        )
    )

    if messages == "many":
        keyboard.add(
            InlineKeyboardButton(
                text=_("Отменить"),
                callback_data=cancel_moderate_callback.new(
                    user_id=contact_id
                )
            )
        )
    return keyboard


def cancel_moderate(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Завершить сеанс"),
                    callback_data=cancel_moderate_callback.new(
                        user_id=user_id
                    )
                )
            ]
        ]
    )
