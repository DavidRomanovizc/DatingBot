from functions.get_data_func import get_data_meetings
from keyboards.inline.calendar import SimpleCalendar, calendar_callback
from keyboards.inline.game_inline import game_keyboard
from keyboards.inline.payments_inline import payments_keyboard

import asyncio
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from glQiwiApi import types as qiwi_types

from loader import wallet, dp, bot
from utils.db_api import db_commands


# TODO: Изменить структуру.
#  Пользователь проходит верификацию --> выбирает свободною дату, которую создал админ и только потом оплачивает
#  Добавить перевод текста
async def create_payment(amount: Union[float, int] = 600) -> qiwi_types.Bill:
    async with wallet:
        return await wallet.create_p2p_bill(amount=amount)


@dp.callback_query_handler(text="pay_balance")
async def get_payment(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text("<b>💳 Стоимость подписки:</b>\n"
                                 "├Навсегда 600\n"
                                 "├Чтобы проверить актуальность цен, нажмите на кнопку \n<b>├🔄 Проверить цены</b>\n"
                                 "├Если у вас нет Qiwi или нет возможности оплатить с помощью ├киви,"
                                 " напишите агенту поддержки",
                                 reply_markup=await payments_keyboard())


@dp.callback_query_handler(text="check_price")
async def check_price(call: CallbackQuery):
    await bot.answer_callback_query(call.id, text="✔️ Цена актуальна")


@dp.callback_query_handler(text='pay_qiwi')
async def payment(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    user_data = await get_data_meetings(call.from_user.id)
    user_premium = user_data[5]
    bill = await create_payment()
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Оплатить', url=bill.pay_url)
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Проверить оплату', callback_data='check_payment')
    keyboard.add(btn2)
    btn3 = types.InlineKeyboardButton(text='Отмена', callback_data='cancel_payment')
    keyboard.add(btn3)
    if user_premium is True:
        await bot.send_message(call.from_user.id, text=f"Поздравляю! Доступ уже куплен :)")
        await asyncio.sleep(1)
        await bot.send_message(call.from_user.id, text=f"👑 Приветствуем вас, {call.from_user.full_name}!\n\n"
                                                       f"🖥️ Это система для решения <b>онлайн тестов</b> на "
                                                       f"образовательных платформах РФ\n\n ",
                               reply_markup=await game_keyboard(user_premium))

    else:
        await bot.send_message(call.from_user.id, text=f"После оплаты нажми <b>Проверить оплату</b>\n"
                                                       f"Если не получается оплатить по странице ниже",
                               reply_markup=keyboard)
        await state.set_state("payment")
        await state.update_data(bill=bill)


@dp.callback_query_handler(state="payment", text="check_payment")
async def successful_payment(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Проверить оплату', callback_data='check_payment')
    keyboard.add(btn1)
    keyboard1 = types.ReplyKeyboardMarkup()
    async with state.proxy() as data:
        bill: qiwi_types.Bill = data.get("bill")
    status = await bill.check()
    if status:
        await call.message.edit_text("Оплата прошла успешно!")
        await db_commands.update_user_meetings_data(telegram_id=call.from_user.id, is_premium=True)
        await state.finish()
    else:
        await call.message.answer("Оплата не прошла! Подождите минут 10, а затем еще раз попробуйте нажать кнопку ниже",
                                  reply_markup=keyboard)


@dp.callback_query_handler(state='payment', text='cancel_payment')
async def cancel_payment(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    user_data = await get_data_meetings(call.from_user.id)
    user_premium = user_data[5]
    await call.message.reply(f'Вы отменили покупку :(\n', reply_markup=await game_keyboard(user_premium))
    await state.reset_state()


@dp.callback_query_handler(text="choice_the_date")
async def handled_purchase(call: CallbackQuery):
    await call.message.edit_text("Пожалуйста, выберите дату: ", reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(calendar_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}'
        )
