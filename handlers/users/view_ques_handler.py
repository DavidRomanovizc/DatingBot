import asyncio
import random
import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from functions.create_forms_funcs import create_questionnaire, create_questionnaire_reciprocity
from functions.get_data_func import get_data
from functions.get_next_user_func import get_next_user
from handlers.users.back_handler import delete_message
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.questionnaires_inline import action_keyboard, action_reciprocity_keyboard
from keyboards.inline.registration_inline import registration_keyboard
from loader import dp
from utils.db_api import db_commands


@dp.callback_query_handler(text='find_ancets')
async def start_finding(call: CallbackQuery, state: FSMContext):
    try:
        telegram_id = call.from_user.id
        user_data = await get_data(telegram_id)
        user_list = await get_next_user(telegram_id)
        user_status = user_data[9]
        if user_status:
            random_user = random.choice(user_list)
            await delete_message(call.message)
            await create_questionnaire(form_owner=random_user, chat_id=telegram_id)
            await state.set_state('finding')
        else:
            await call.message.edit_text("Вам необходимо зарегистрироваться, нажмите на кнопку ниже",
                                         reply_markup=await registration_keyboard())
    except IndexError:
        await call.answer("На данный момент у нас нет подходящих анкет для вас")


@dp.callback_query_handler(action_keyboard.filter(action=["like", "dislike", "stopped"]),
                           state='finding')
async def like_questionnaire(call: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    user_list = await get_next_user(call.from_user.id)
    random_user = random.choice(user_list)
    action = callback_data['action']
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    username = call.from_user.username
    if action == "like":
        try:
            target_id = callback_data["target_id"]
            await create_questionnaire(form_owner=call.from_user.id, chat_id=target_id,
                                       add_text=f'Вами заинтересовался пользователь '
                                                f'<a href="https://t.me/{username}">{username}</a>')
            await create_questionnaire(form_owner=random_user, chat_id=call.from_user.id)

            await state.reset_data()
        except Exception as err:
            logger.error(err)
            await create_questionnaire(form_owner=random_user, chat_id=call.from_user.id)
    elif action == "dislike":
        try:
            await create_questionnaire(form_owner=random_user, chat_id=call.from_user.id)
            await state.reset_data()
        except Exception as err:
            logger.error(err)
            await create_questionnaire(form_owner=random_user, chat_id=call.from_user.id)
    elif action == "stopped":
        markup = await start_keyboard(user_db["status"])
        await call.message.delete()
        await call.message.answer(f"Рад был помочь, {call.from_user.full_name}!\n"
                                  f"Надеюсь, ты нашел кого-то благодаря мне", reply_markup=markup)
        await state.reset_state()


@dp.callback_query_handler(action_reciprocity_keyboard.filter(action=["like_reciprocity", "dislike_reciprocity"]))
async def like_questionnaire_reciprocity(call: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    action = callback_data['action']
    username = call.from_user.username
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    if action == "like_reciprocity":
        user_for_like = callback_data["user_for_like"]
        user_db = await db_commands.select_user(telegram_id=call.from_user.id)
        await asyncio.sleep(1)
        await call.message.delete()
        await call.message.answer("Ваша анкета отправлена другому пользователю",
                                  reply_markup=await start_keyboard(user_db["status"]))
        await asyncio.sleep(5)
        await create_questionnaire_reciprocity(liker=call.from_user.id, chat_id=user_for_like,
                                               add_text=f'Вам ответили взаимностью, пользователь - '
                                                        f'<a href="https://t.me/{username}">{username}</a>',
                                               user_db=user_db)
        await state.reset_state()
    elif action == "dislike_reciprocity":
        await asyncio.sleep(1)
        await delete_message(call.message)
        await call.message.answer("Меню: ", reply_markup=await start_keyboard(user_db["status"]))
        await state.reset_state()
    await state.reset_state()


@dp.callback_query_handler(text="go_back_to_viewing_ques", state='finding')
async def like_questionnaire(call: CallbackQuery, state: FSMContext):
    user_list = await get_next_user(call.from_user.id)
    random_user = random.choice(user_list)

    try:
        await create_questionnaire(form_owner=random_user, chat_id=call.from_user.id)

        await state.reset_data()
    except Exception as err:
        logger.error(err)
        await create_questionnaire(form_owner=random_user, chat_id=call.from_user.id)


@dp.message_handler(state='finding')
async def echo_message_finding(message: types.Message, state: FSMContext):
    user_db = await db_commands.select_user(telegram_id=message.from_user.id)
    await message.answer("Меню: ", reply_markup=await start_keyboard(user_db["status"]))
    await state.reset_state(with_data=True)