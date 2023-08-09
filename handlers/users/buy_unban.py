from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.admin_inline import unban_user_keyboard
from keyboards.inline.payments_inline import payments_keyboard
from loader import dp, bot, _


@dp.callback_query_handler(text="unban")
async def get_payment(call: CallbackQuery) -> None:
    await call.answer(cache_time=60)
    await call.message.edit_text(
        text=_("<b>💳 Стоимость разбана - 600</b>\n"
               "├Чтобы проверить актуальность цен, нажмите на кнопку \n<b>├🔄 Проверить цены</b>\n"
               "├Если у вас нет Qiwi или нет возможности\n├оплатить с помощью киви,"
               " напишите агенту поддержки"),
        reply_markup=await payments_keyboard("unban")
    )


@dp.callback_query_handler(text="check_price")
async def check_price(call: CallbackQuery) -> None:
    await bot.answer_callback_query(call.id, text=_("✔️ Цена актуальна"))


@dp.callback_query_handler(text='pay_qiwi')
async def payment(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer(cache_time=60)


@dp.callback_query_handler(state="payment", text="check_payment")
async def successful_payment(call: CallbackQuery, state: FSMContext) -> None:
    ...


@dp.callback_query_handler(state='payment', text='cancel_payment')
async def cancel_payment(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer(cache_time=60)
    await call.message.edit_text(_("Вы забанены!"), reply_markup=await unban_user_keyboard())
    await state.reset_state()
