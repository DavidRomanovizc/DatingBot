import asyncio
import random
import typing

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from handlers.users.back_handler import delete_message
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.questionnaires_inline import questionnaires_keyboard, action_keyboard, action_reciprocity_keyboard
from loader import dp
from utils.db_api import db_commands
from utils.misc.create_questionnaire import get_data, find_user_gender, send_questionnaire


async def select_all_users_list():
    users_records = await db_commands.select_all_users()
    list_id = []
    for i in users_records:
        id_user = i.get('telegram_id')
        list_id.append(id_user)
    return list_id


async def create_questionnaire(state, random_user, chat_id, add_text=None):
    markup = await questionnaires_keyboard()
    user_data = await get_data(random_user)
    await send_questionnaire(chat_id=chat_id, user_data=user_data, markup=markup, add_text=add_text)
    await state.update_data(data={'questionnaire_owner': random_user})


async def create_questionnaire_reciprocity(state, random_user, chat_id, add_text=None):
    user_data = await get_data(random_user)
    await send_questionnaire(chat_id=chat_id, user_data=user_data, add_text=add_text)
    await state.update_data(data={'questionnaire_owner': random_user})


@dp.callback_query_handler(text='find_ancets')
async def start_finding(call: CallbackQuery, state: FSMContext):
    await delete_message(call.message)
    user_list = await find_user_gender(call.from_user.id)
    random_user = random.choice(user_list)
    await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)
    await state.set_state('finding')


@dp.callback_query_handler(action_keyboard.filter(action=["like", "dislike", "stopped"]),
                           state='finding')
async def like_questionnaire(call: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    user_list = await find_user_gender(call.from_user.id)
    random_user = random.choice(user_list)
    action = callback_data['action']

    await state.update_data(data={'questionnaire_owner': random_user})
    username = call.from_user.username
    like_from_user = call.from_user.id
    liked_user = await state.get_data('questionnaire_owner')
    liked_user = liked_user.get('questionnaire_owner')
    if action == "like":
        try:
            await create_questionnaire(random_user=like_from_user, chat_id=liked_user,
                                       add_text=f'Вами заинтересовался пользователь '
                                                f'<a href="https://t.me/{username}">{username}</a>',
                                       state=state)
            await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)

            await state.reset_data()
        except Exception as err:
            logger.error(err)
            await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)
    elif action == "dislike":
        try:
            await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)
            await state.reset_data()
        except Exception as err:
            logger.error(err)
            await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)
    elif action == "stopped":
        markup = await start_keyboard()
        await call.message.delete()
        await call.message.answer(f"Рад был помочь, {call.from_user.full_name}!\n"
                                  f"Надеюсь, ты нашел кого-то благодаря мне", reply_markup=markup)
        await state.reset_state()


@dp.callback_query_handler(action_reciprocity_keyboard.filter(action=["like_reciprocity", "dislike_reciprocity"]))
async def like_questionnaire_reciprocity(call: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    user_list = await find_user_gender(call.from_user.id)
    random_user = random.choice(user_list)
    action = callback_data['action']

    await state.update_data(data={'questionnaire_owner': random_user})
    username = call.from_user.username
    like_from_user = call.from_user.id
    liked_user = await state.get_data('questionnaire_owner')
    liked_user = liked_user.get('questionnaire_owner')
    if action == "like_reciprocity":
        await asyncio.sleep(1)
        await delete_message(call.message)
        await call.message.answer("Ваша анкета отправлена другому пользователю", reply_markup=await start_keyboard())
        await create_questionnaire_reciprocity(random_user=like_from_user, chat_id=liked_user,
                                               add_text=f'Вам ответили взаимностью, пользователь - '
                                                        f'<a href="https://t.me/{username}">{username}</a>',
                                               state=state)
        await state.reset_state()
    elif action == "dislike_reciprocity":
        await asyncio.sleep(1)
        await delete_message(call.message)
        await call.message.answer("Меню: ", reply_markup=await start_keyboard())
        await state.reset_state()
    await state.reset_state()


@dp.callback_query_handler(text="go_back_to_viewing_ques", state='finding')
async def like_questionnaire(call: CallbackQuery, state: FSMContext):
    user_list = await find_user_gender(call.from_user.id)
    random_user = random.choice(user_list)

    await state.update_data(data={'questionnaire_owner': random_user})
    try:
        await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)

        await state.reset_data()
    except Exception as err:
        logger.error(err)
        await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)
