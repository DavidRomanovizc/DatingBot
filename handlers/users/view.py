from loguru import logger

from keyboards.inline.questionnaires_inline import questionnaires_inline_kb
from keyboards.inline.main_menu import inline_start
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loader import dp, db, bot
from aiogram import types
import random


async def select_all_users_list():
    users_records = await db.select_all_users_id()
    list_id = []
    for i in users_records:
        id_user = i.get('telegram_id')
        list_id.append(id_user)
    return list_id


async def create_questionnaire(state, random_user, chat_id, add_text=None):
    user_data = await db.select_user(telegram_id=random_user)
    varname = user_data.get('varname')
    age = user_data.get('age')
    sex = user_data.get('sex')
    city = user_data.get('city')
    need_partner_sex = user_data.get('need_partner_sex')
    commentary = user_data.get('commentary')
    photo_random_user = user_data.get('photo_id')
    if photo_random_user is None:
        photo_random_user = "https://www.meme-arsenal.com/memes/5eae5104f379baa355e031fa1ded886c.jpg"

    description_random_user = f'{add_text}\n\n' \
                              f'<b>Имя</b> - {varname},\n<b>Возраст</b> - {age},\n<b>Пол</b> - {sex}\n' \
                              f'<b>Город</b> - {city}\n' \
                              f'<b>Ищу</b> - {need_partner_sex}\n\n' \
                              f'<b>О себе:</b>\n{commentary}\n\n'

    await bot.send_photo(chat_id=chat_id, photo=photo_random_user,
                         caption=description_random_user, reply_markup=questionnaires_inline_kb)
    await state.update_data(data={'questionnaire_owner': random_user})


@dp.callback_query_handler(text='find_ancets')
async def start_finding(call: CallbackQuery, state: FSMContext):
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
                                       add_text=f"{answer}", state=state)
            await create_questionnaire(random_user=random_user, chat_id=message.from_user.id, state=state)
            await state.reset_data()
        except Exception as err:
            logger.error(err)
            await create_questionnaire(random_user=random_user, chat_id=message.from_user.id, state=state)


@dp.callback_query_handler(text='stop_finding', state='finding')
async def stop_finding(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f"Рад был помочь, {call.from_user.full_name}!\n"
                              f"Надеюсь, ты нашел кого-то благодаря мне", reply_markup=inline_start)
    await state.reset_state()
