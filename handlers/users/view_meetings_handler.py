import random

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.back_handler import delete_message
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.meeting_inline import reaction_meetings_keyboard
from loader import dp
from utils.db_api import db_commands
from functions.select_all_users_func import select_all_users_list
from functions.meetings_funcs import get_meeting_data, send_ques_meeting


async def create_ques_meeting(state, random_user, chat_id):
    markup = await reaction_meetings_keyboard()
    user_data = await get_meeting_data(random_user)
    await send_ques_meeting(chat_id=chat_id, user_data=user_data, markup=markup)
    await state.update_data(data={'questionnaire_owner': random_user})


@dp.callback_query_handler(text="view_ques")
async def view_meetings(call: CallbackQuery, state: FSMContext):
    await delete_message(call.message)
    user_list = await select_all_users_list(call.from_user.id)
    random_user = random.choice(user_list)
    await create_ques_meeting(random_user=random_user, chat_id=call.from_user.id, state=state)
    await state.set_state('finding_meetings')


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

