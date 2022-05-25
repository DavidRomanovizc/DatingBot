import asyncio
import random
import typing

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from handlers.users.back_handler import delete_message
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.questionnaires_inline import action_keyboard, action_reciprocity_keyboard
from keyboards.inline.registration_inline import registration_keyboard
from loader import dp
from utils.misc.create_questionnaire import find_user_gender, create_questionnaire, create_questionnaire_reciprocity, \
    get_data


@dp.callback_query_handler(text='find_ancets')
async def start_finding(call: CallbackQuery, state: FSMContext):
    try:
        telegram_id = call.from_user.id
        user_data = await get_data(telegram_id)
        user_list = await find_user_gender(telegram_id)
        user_status = user_data[9]
        if user_status:
            random_user = random.choice(user_list)
            await delete_message(call.message)
            await create_questionnaire(random_user=random_user, chat_id=telegram_id, state=state)
            await state.set_state('finding')
        else:
            await call.message.edit_text("Вам необходимо зарегистрироваться, нажмите на кнопку ниже",
                                         reply_markup=await registration_keyboard())
    except IndexError:
        await call.answer("На данный момент у нас нет подходящих анкет для вас")


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
