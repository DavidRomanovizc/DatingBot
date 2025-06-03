import random
import secrets
from typing import (
    Optional,
)

from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
)
from aiogram.utils.exceptions import (
    BadRequest,
)

from functions.dating.get_next_user_func import (
    get_next_user,
)
from functions.dating.send_form_func import (
    send_questionnaire,
)
from keyboards.inline.questionnaires_inline import (
    questionnaires_keyboard,
)
from loader import (
    bot,
)


async def create_questionnaire(
        form_owner: int,
        chat_id: int,
        add_text: Optional[str] = None,
        monitoring: bool = False,
        report_system: bool = False,
) -> None:
    markup = await questionnaires_keyboard(target_id=form_owner, monitoring=monitoring)
    await send_questionnaire(
        chat_id=chat_id,
        markup=markup,
        add_text=add_text,
        monitoring=monitoring,
        report_system=report_system,
        owner_id=form_owner,
    )


async def create_questionnaire_reciprocity(
        liker: int, chat_id: int, add_text: str = None
) -> None:
    await send_questionnaire(chat_id=chat_id, add_text=add_text, owner_id=liker)


async def monitoring_questionnaire(call: CallbackQuery, state: FSMContext) -> None:
    telegram_id = call.from_user.id
    storage = await state.get_data()
    user_offsets = storage.get("user_offsets", dict())
    user_limits = storage.get("user_limits", dict())
    offset = user_offsets.get(telegram_id, 0)
    limit = user_limits.get(telegram_id, 100)
    user_list = await get_next_user(telegram_id, monitoring=True, offset=offset, limit=limit)

    if user_list:
        user_offsets[telegram_id] = offset + len(user_list)
    user_limits[telegram_id] = limit + 100
    await state.update_data(user_offsets=user_offsets)
    random_user = random.choice(user_list)
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    try:
        await create_questionnaire(
            form_owner=random_user, chat_id=telegram_id, monitoring=True
        )
    except BadRequest:
        await create_questionnaire(
            form_owner=random_user, chat_id=telegram_id, monitoring=True
        )


async def rand_user_list(call: CallbackQuery) -> int:
    user_list = await get_next_user(call.from_user.id)
    random_user_list = [random.choice(user_list) for _ in range(len(user_list))]
    random_user = secrets.choice(random_user_list)
    return random_user
