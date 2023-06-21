import random
import secrets
from typing import NoReturn

import numpy as np
from aiogram.types import CallbackQuery

from functions.dating.get_next_user_func import get_next_user
from functions.dating.send_form_func import send_questionnaire
from handlers.users.back_handler import delete_message
from keyboards.inline.questionnaires_inline import questionnaires_keyboard
from keyboards.inline.registration_inline import registration_keyboard
from loader import _
from utils.db_api import db_commands


async def create_questionnaire(form_owner: int, chat_id: str, add_text=None, monitoring=False,
                               report_system=False) -> None:
    markup = await questionnaires_keyboard(target_id=form_owner, monitoring=monitoring)
    await send_questionnaire(chat_id=chat_id, markup=markup, add_text=add_text,
                             monitoring=monitoring, report_system=report_system, owner_id=form_owner)


async def create_questionnaire_reciprocity(liker: int, chat_id: str, add_text=None) -> None:
    await send_questionnaire(chat_id=chat_id, add_text=add_text, owner_id=liker)


async def monitoring_questionnaire(call: CallbackQuery) -> NoReturn:
    try:
        telegram_id = call.from_user.id
        user = await db_commands.select_user(telegram_id)
        user_list = await get_next_user(telegram_id, call, monitoring=True)
        user_status = user.get("status")
        if user_status:
            random_user = random.choice(user_list)
            await delete_message(call.message)
            await create_questionnaire(form_owner=random_user, chat_id=telegram_id, monitoring=True)
        else:
            await call.message.edit_text(_("Вам необходимо зарегистрироваться, нажмите на кнопку ниже"),
                                         reply_markup=await registration_keyboard())
    except IndexError:
        await call.answer(_("На данный момент у нас нет подходящих анкет для вас"))


async def rand_user_list(call: CallbackQuery) -> int:
    user_list = await get_next_user(call.from_user.id, call)
    random_user_list = [np.random.choice(user_list) for _ in range(len(user_list))]
    random_user = secrets.choice(random_user_list)
    return random_user
