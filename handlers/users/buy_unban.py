from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.payments_inline import payments_keyboard, making_payment
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from glQiwiApi import types as qiwi_types

from loader import wallet, dp, bot, _
from utils.db_api import db_commands


async def create_payment(amount: Union[float, int] = 1) -> qiwi_types.Bill:
    async with wallet:
        return await wallet.create_p2p_bill(amount=amount)


@dp.callback_query_handler(text="unban")
async def get_payment(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text(_("<b>💳 Стоимость разбана - 600</b>\n"
                                   "├Чтобы проверить актуальность цен, нажмите на кнопку \n<b>├🔄 Проверить цены</b>\n"
                                   "├Если у вас нет Qiwi или нет возможности оплатить с помощью ├киви,"
                                   " напишите агенту поддержки"),
                                 reply_markup=await payments_keyboard("unban"))


@dp.callback_query_handler(text="check_price")
async def check_price(call: CallbackQuery):
    await bot.answer_callback_query(call.id, text=_("✔️ Цена актуальна"))


@dp.callback_query_handler(text='pay_qiwi')
async def payment(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    bill = await create_payment()

    await bot.send_message(call.from_user.id, text=_(f"После оплаты нажмите <b>Проверить оплату</b>\n"
                                                     f"Если не получается оплатить по странице ниже"),
                           reply_markup=await making_payment(bill))
    await state.set_state("payment")
    await state.update_data(bill=bill)


@dp.callback_query_handler(state="payment", text="check_payment")
async def successful_payment(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=_("Проверить оплату"), callback_data='check_payment')
    keyboard.add(btn1)
    keyboard1 = types.ReplyKeyboardMarkup()
    async with state.proxy() as data:
        bill: qiwi_types.Bill = data.get("bill")
    status = await bill.check()
    if status:
        await call.message.edit_text(_("Оплата прошла успешно!"))
        await db_commands.update_user_data(telegram_id=call.from_user.id, is_banned=False)
        await state.finish()
    else:
        await call.message.answer(_("Оплата не прошла! Подождите минут 10, а затем еще раз попробуйте нажать кнопку "
                                    "ниже"),
                                  reply_markup=keyboard)


@dp.callback_query_handler(state='payment', text='cancel_payment')
async def cancel_payment(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.reply(_("Вы отменили покупку :("), reply_markup=await start_keyboard(call.from_user.id))
    await state.reset_state()
