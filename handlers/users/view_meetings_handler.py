import random

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from functions.meetings_funcs import create_ques_meeting
from handlers.users.back_handler import delete_message
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp
from utils.db_api import db_commands
from functions.select_all_users_func import select_all_users_list


@dp.callback_query_handler(text="view_ques")
async def view_meetings(call: CallbackQuery, state: FSMContext):
    try:
        await delete_message(call.message)
        user_list = await select_all_users_list(call.from_user.id)
        random_user = random.choice(user_list)
        await create_ques_meeting(random_user=random_user, chat_id=call.from_user.id, state=state)
        await state.set_state('finding_meetings')
    except IndexError:
        await call.message.answer("На данный момент у нас нет подходящих анкет для вас")


@dp.callback_query_handler(state="finding_meetings", text="further")
async def like_questionnaire_reciprocity(call: CallbackQuery, state: FSMContext):
    user_list = await select_all_users_list(call.from_user.id)
    random_user = random.choice(user_list)
    await create_ques_meeting(state=state, random_user=random_user, chat_id=call.from_user.id)


@dp.callback_query_handler(state='finding_meetings', text="stopped")
async def like_questionnaire(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    markup = await start_keyboard(status=user_db['status'])
    await call.message.delete()
    await call.message.answer(f"Рад был помочь, {call.from_user.full_name}!\n"
                              f"Надеюсь, ты нашел кого-то благодаря мне", reply_markup=markup)
    await state.reset_state()
