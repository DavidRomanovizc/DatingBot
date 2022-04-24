import asyncio
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import support_ids
from handlers.users.view_ques_handler import create_questionnaire, select_all_users_list
from keyboards.inline.admin_inline import banned_user_keyboard
from loader import dp, bot
from states.reports import Report
from utils.misc.create_questionnaire import get_data


@dp.callback_query_handler(text="send_report", state='finding')
async def report_user(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer(
        "Напишите причину жалобы\n")
    await Report.R1.set()


@dp.message_handler(state=Report.R1)
async def report_user(message: types.Message, state: FSMContext):
    display_name = message.from_user.full_name
    user_list = await select_all_users_list()
    user_list.remove(message.from_user.id)
    print(user_list)
    random_user = random.choice(user_list)
    markup = await banned_user_keyboard()

    for supp_id in support_ids:
        user_data = await get_data(random_user)
        await bot.send_photo(chat_id=supp_id, caption=f"<b>Жалоба</b> - {message.text}\n\n"
                                                      f"<b>Статус анкеты</b> - \n{str(user_data[12])}\n"
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
    await message.answer(
        f"Репорт на пользователя успешно отправлен.\nАдминистрация предпримет все необходимые меры",
        reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(3)
    async with state.proxy() as data:
        data["report_us"] = display_name
        await create_questionnaire(random_user=random_user, chat_id=message.from_user.id, state=state)
        await state.set_state('finding')
