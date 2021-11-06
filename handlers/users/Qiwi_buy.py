from keyboards.inline.inline_start_menu import inline_start
from utils.misc.QIWI import Payment, NoPaymentFound, NotEnoughMoney
from keyboards.inline.Primer import paid_keyboard, prime_buy
from aiogram.utils.markdown import hcode, hlink
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from data.subs import items
from aiogram import types
from data import config
from loader import dp


@dp.callback_query_handler(text_contains="qiwi_pay")
async def show_items(call: CallbackQuery):
    await call.answer(cache_time=60)
    caption = """
Название продукта: {title}
<i>Описание:</i>
{description}
<u>Цена:</u> {price:.2f} <b>RUB</b>
"""

    for item in items:
        await call.message.answer_photo(
            photo=item.photo_link,
            caption=caption.format(
                title=item.title,
                description=item.description,
                price=item.price,
            ),
            reply_markup=prime_buy(item_id=item.id)
        )


@dp.callback_query_handler(text_contains="buy")
async def create_invoice(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    item_id = call.data.split(":")[-1]
    item_id = int(item_id) - 1
    item = items[item_id]

    amount = item.price
    payment = Payment(amount=amount)
    payment.create()

    await call.message.answer(
        "\n".join([
            f"Оплатите не менее {amount:.2f} по номеру телефона или по адресу",
            "",
            hlink(config.WALLET_QIWI, url=payment.invoice),
            "\nИ обязательно укажите ID платежа:\n",
            hcode(payment.id)
        ]),
        reply_markup=paid_keyboard)

    await state.set_state("qiwi")
    await state.update_data(payment=payment)

    @dp.callback_query_handler(text="cancel_2", state="qiwi")
    async def cancel_payment(call: types.CallbackQuery, state: FSMContext):
        await call.message.edit_text("Отменено. Вы были автоматически возвращены в меню", reply_markup=inline_start)
        await state.finish()

    @dp.callback_query_handler(text="paid", state="qiwi")
    async def approve_payment(call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        payment: Payment = data.get("payment")
        try:
            payment.check_payment()
        except NoPaymentFound:
            await call.message.answer("Транзакция не найдена.")
            return
        except NotEnoughMoney:
            await call.message.answer("Оплаченная сума меньше необходимой.")
            return

        else:
            await call.message.answer("Успешно оплачено")
        await call.message.edit_reply_markup()
        await state.finish()
