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


async def select_all_users_list():
    users_records = await db_commands.select_all_users()
    list_id = []
    for i in users_records:
        id_user = i.get('telegram_id')
        list_id.append(id_user)
    return list_id


async def create_questionnaire(state, random_user, chat_id, add_text=None):
    markup = await questionnaires_keyboard()
    user_data = await db_commands.select_user(telegram_id=random_user)
    varname = user_data.get('varname')
    age = user_data.get('age')
    sex = user_data.get('sex')
    city = user_data.get('city')
    need_partner_sex = user_data.get('need_partner_sex')
    commentary = user_data.get('commentary')
    photo_random_user = user_data.get('photo_id')
    if photo_random_user is None:
        photo_random_user = "https://www.meme-arsenal.com/memes/5eae5104f379baa355e031fa1ded886c.jpg"
    # TODO: изменить оформление анкеты
    description_random_user = (f'<b>Имя</b> - {varname},\n<b>Возраст</b> - {age},\n<b>Пол</b> - {sex}\n'
                               f'<b>Город</b> - {city}\n'
                               f'<b>Ищу</b> - {need_partner_sex}\n\n'
                               f'<b>О себе:</b>\n{commentary}\n\n')
    await bot.send_photo(chat_id=chat_id, photo=photo_random_user,
                         caption=description_random_user, reply_markup=markup)
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
