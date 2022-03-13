##############################################
#                FROZEN                     ##
#             INDEFINITELY                  ##
#############################################
from aiogram import types
from aiogram.types import CallbackQuery, ContentTypes

from data.config import UTOKEN
from keyboards.inline.Primer import choice_payment
from keyboards.inline.main_menu import inline_start
from loader import dp, bot


@dp.callback_query_handler(text="Donation")
async def show_items(call: CallbackQuery):
    await call.message.edit_text("Выберите способ оплаты", reply_markup=choice_payment)


@dp.callback_query_handler(text="ykassa_pay")
async def buy_sub(call: CallbackQuery):
    await bot.send_invoice(chat_id=call.from_user.id, title="Спонсорка", description="Описание возможностей: ",
                           payload="month_sub", provider_token=UTOKEN, currency="RUB",
                           start_parameter="test_bot",
                           prices=[{"label": "Руб", "amount": 10000}])


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pcq: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pcq.id, ok=True)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        await message.answer("Вам выдана подписка на месяц")
