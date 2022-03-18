import asyncio
import random

from aiogram import types

from handlers.users.view_ques import create_questionnaire, select_all_users_list
from keyboards.inline.report_button import report_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.second_menu import second_menu_keyboard
from states.reports import Report
from data.config import ADMINS
from loader import dp, bot


@dp.callback_query_handler(text="send_report", state='finding')
async def report_user(call: CallbackQuery):
    markup = await report_keyboard()
    await call.answer(cache_time=60)
    await call.message.answer(
        "Укажите причину жалобы\n"
        "\n"
        "1. 🔞 Материал для взрослых.\n"
        "2. 💊 Пропаганда наркотиков.\n"
        "3. 💰 Продажа товаров и услуг.\n"
        "4. 🦨 Другое.\n"
        "\n"
        "5. Вернуться назад.", reply_markup=markup)
    await Report.R1.set()


@dp.callback_query_handler(state=Report.R1)
async def report_user(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    display_name = call.from_user.full_name
    user_list = await select_all_users_list()
    random_user = random.choice(user_list)

    for admin_id in ADMINS:
        if call.data == "content":
            await bot.send_message(
                admin_id,
                f"Кинут репорт на пользователя за 18+ контент\n"
            )
        elif call.data == "drugs":
            await bot.send_message(
                admin_id,
                f"Кинут репорт на пользователя за публикацию/продажу и т.д наркотиков\n"
            )
        elif call.data == "scam":
            await bot.send_message(admin_id, f"Кинут репорт на пользователя за мошенничество\n")
        elif call.data == "another":
            await bot.send_message(
                admin_id,
                f"Кинут репорт на пользователя за другое\n"
            )

    await call.message.answer(
        f"Репорт на пользователя успешно отправлен.\nАдминистрация предпримет все необходимые меры",
        reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(3)
    async with state.proxy() as data:
        data["report_us"] = display_name
        await create_questionnaire(random_user=random_user, chat_id=call.from_user.id, state=state)
        await state.set_state('finding')


@dp.callback_query_handler(text="cancel_report", state=Report.R1)
async def cancel_report(call: CallbackQuery, state: FSMContext):
    markup = await second_menu_keyboard()
    await call.message.delete()
    await call.message.answer("Вы вернулись в меню", reply_markup=markup)
    await state.finish()
