from aiogram.types import CallbackQuery

from keyboards.inline.questionnaires_inline import questionnaires_inline_kb
from loader import dp, db, bot
import random


async def select_all_users_list():
    users_records = await db.select_all_users_id()
    list_id = []
    for i in users_records:
        id_user = i.get('telegram_id')
        list_id.append(id_user)
    return list_id


async def create_questionnaire(user_list, need_sex, message):
    random_user = random.choice(user_list)
    user_data = await db.select_user(telegram_id=random_user)
    varname = user_data.get('varname')
    age = user_data.get('age')
    sex = user_data.get('sex')
    city = user_data.get('city')
    commentary = user_data.get('commentary')
    photo_random_user = user_data.get('photo_id')
    description_random_user = f'{varname}, {age}, {sex}\n' \
                              f'{city}\n' \
                              f'{commentary}\n\n'
    await bot.send_photo(chat_id=message.from_user.id, photo=photo_random_user,
                         caption=description_random_user, reply_markup=questionnaires_inline_kb)


@dp.callback_query_handler(text='find_ancets')
async def start_finding(call: CallbackQuery):
    await call.answer(cache_time=60)
    user_list = await select_all_users_list()
    await create_questionnaire(user_list=user_list, need_sex=None, message=call)
