from loguru import logger

from handlers.users.back_handler import delete_message
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.questionnaires_inline import questionnaires_keyboard

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loader import dp, bot
from aiogram import types
import random

from utils.db_api import db_commands
from utils.misc.create_questionnaire import get_data


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
    await bot.send_photo(chat_id=chat_id, caption=f"<b>Статус анкеты</b> - \n{str(user_data[12])}\n\n"
                                                  f"<b>Имя</b> - {str(user_data[0])}\n"
                                                  f"<b>Возраст</b> - {str(user_data[1])}\n"
                                                  f"<b>Пол</b> - {str(user_data[2])}\n"
                                                  f"<b>Национальность</b> - {str(user_data[3])}\n"
                                                  f"<b>Образование</b> - {str(user_data[4])}\n"
                                                  f"<b>Город</b> - {str(user_data[5])}\n"
                                                  f"<b>Наличие машины</b> - {str(user_data[6])}\n"
                                                  f"<b>Наличие жилья</b> - {str(user_data[7])}\n"
                                                  f"<b>Ваше занятие</b> - {str(user_data[8])}\n"
                                                  f"<b>Наличие детей</b> - {str(user_data[9])}\n"
                                                  f"<b>Семейное положение</b> - {str(user_data[10])}\n\n"
                                                  f"<b>О себе</b> - {str(user_data[11])}\n\n",
                         photo=user_data[13], reply_markup=markup)
    await state.update_data(data={'questionnaire_owner': random_user})


@dp.callback_query_handler(text='find_ancets')
async def start_finding(call: CallbackQuery, state: FSMContext):
    await delete_message(call.message)
    user_list = await select_all_users_list()
    user_list.remove(call.from_user.id)
    random_user = random.choice(user_list)
    await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)
    await state.set_state('finding')


@dp.callback_query_handler(text='like_questionnaire', state='finding')
async def like_questionnaire(call: CallbackQuery, state: FSMContext):
    user_list = await select_all_users_list()
    user_list.remove(call.from_user.id)
    random_user = random.choice(user_list)

    await state.update_data(data={'questionnaire_owner': random_user})
    username = call.from_user.username
    like_from_user = call.from_user.id
    liked_user = await state.get_data('questionnaire_owner')
    liked_user = liked_user.get('questionnaire_owner')
    try:
        await create_questionnaire(random_user=like_from_user, chat_id=liked_user,
                                   add_text=f'Вами заинтересовался пользователь \n https://t.me/{username}',
                                   state=state)
        await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)

        await state.reset_data()
    except Exception as err:
        logger.error(err)
        await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)


@dp.callback_query_handler(text='dislike_questionnaire', state='finding')
async def like_questionnaire(call: CallbackQuery, state: FSMContext):
    user_list = await select_all_users_list()
    user_list.remove(call.from_user.id)
    random_user = random.choice(user_list)
    try:
        await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)
        await state.reset_data()
    except Exception as err:
        logger.error(err)
        await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)


@dp.callback_query_handler(text='send_message_questionnaire', state='finding')
async def like_questionnaire(call: CallbackQuery, state: FSMContext):
    user_list = await select_all_users_list()
    user_list.remove(call.from_user.id)
    await call.message.answer("Напиши сообщение для этого пользователя")
    await state.reset_data()


# TODO: Отправка сообщений работает через раз
@dp.message_handler(state='finding')
async def like_questionnaire(message: types.Message, state: FSMContext):
    answer_from_user = message.from_user.id
    answered_user = await state.get_data('questionnaire_owner')
    answered_user = answered_user.get('questionnaire_owner')
    user_list = await select_all_users_list()
    user_list.remove(message.from_user.id)
    random_user = random.choice(user_list)
    answer = message.text
    async with state.proxy() as data:
        data["message"] = answer
        try:
            await create_questionnaire(random_user=answer_from_user, chat_id=answered_user,
                                       add_text=f"У вас новое сообщение: {answer}", state=state)
            await create_questionnaire(random_user=random_user, chat_id=message.from_user.id, state=state)
            await state.reset_data()
        except Exception as err:
            logger.error(err)
            await create_questionnaire(random_user=random_user, chat_id=message.from_user.id, state=state)


@dp.callback_query_handler(text='stop_finding', state='finding')
async def stop_finding(call: CallbackQuery, state: FSMContext):
    markup = await start_keyboard()
    await call.message.delete()
    await call.message.answer(f"Рад был помочь, {call.from_user.full_name}!\n"
                              f"Надеюсь, ты нашел кого-то благодаря мне", reply_markup=markup)
    await state.reset_state()
