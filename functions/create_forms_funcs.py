import random
import secrets
from typing import Tuple, NoReturn

import numpy as np
from aiogram.types import CallbackQuery

from functions.get_data_func import get_data
from functions.get_next_user_func import get_next_user
from functions.send_form_func import send_questionnaire
from handlers.users.back_handler import delete_message
from keyboards.inline.questionnaires_inline import questionnaires_keyboard
from keyboards.inline.registration_inline import registration_keyboard
from utils.db_api import db_commands
from loader import _


async def create_questionnaire(form_owner: int, chat_id: str, add_text=None, monitoring=False,
                               report_system=False) -> NoReturn:
    user_db = await db_commands.select_user(form_owner)
    markup = await questionnaires_keyboard(target_id=form_owner, monitoring=monitoring)
    user_data = await get_data(form_owner)
    await send_questionnaire(chat_id=chat_id, user_data=user_data, markup=markup, add_text=add_text, user_db=user_db,
                             monitoring=monitoring, report_system=report_system)


async def create_questionnaire_reciprocity(liker: int, chat_id: str, add_text=None, user_db=None):
    user_data = await get_data(liker)
    await send_questionnaire(chat_id=chat_id, user_data=user_data, add_text=add_text, user_db=user_db)


async def monitoring_questionnaire(call: CallbackQuery) -> NoReturn:
    try:
        telegram_id = call.from_user.id
        user_data = await get_data(telegram_id)
        user_list = await get_next_user(telegram_id, call, monitoring=True)
        user_status = user_data[9]
        if user_status:
            random_user = random.choice(user_list)
            await delete_message(call.message)
            await create_questionnaire(form_owner=random_user, chat_id=telegram_id, monitoring=True)
        else:
            await call.message.edit_text(_("Вам необходимо зарегистрироваться, нажмите на кнопку ниже"),
                                         reply_markup=await registration_keyboard())
    except IndexError:
        await call.answer(_("На данный момент у нас нет подходящих анкет для вас"))


async def rand_user_list(call: CallbackQuery) -> Tuple[int, int, int, int]:
    user_list = await get_next_user(call.from_user.id, call)
    user_list_update = sorted(user_list, key=lambda A: random.random())
    random_user_1 = np.random.choice(user_list_update)
    random_user_2 = np.random.choice(user_list)
    random_user_3 = secrets.choice(user_list_update)
    random_user_list = [random_user_1, random_user_2, random_user_3]
    random_user_list_update = sorted(random_user_list, key=lambda A: random.random())
    rand_user = random.choice(random_user_list_update)
    return random_user_1, random_user_2, random_user_3, rand_user
