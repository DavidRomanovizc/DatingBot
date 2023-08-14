from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import load_config
from keyboards.inline.admin_inline import unban_user_keyboard
from keyboards.inline.payments_inline import payments_keyboard
from loader import dp, bot, _, wallet
from utils.db_api import db_commands
from utils.yoomoney.types import PaymentSource


@dp.callback_query_handler(text="unban")
async def get_payment(call: CallbackQuery) -> None:
    await call.answer(cache_time=60)
    payment_form = await wallet.create_payment_form(
        amount_rub=1,
        unique_label="Dating",
        payment_source=PaymentSource.YOOMONEY_WALLET,
        success_redirect_url=load_config().misc.redirect_url,
    )
    payment_is_completed: bool = await wallet.check_payment_on_successful(payment_form.payment_label)
    print(payment_is_completed)
    await call.message.edit_text(
        text=_(
            "<b>💳 Стоимость разбана - 600</b>\n"
            "├Чтобы проверить актуальность цен, нажмите на кнопку \n"
            "├🔄 Проверить цены\n"
            "├Оплата обычно приходить в течение 1-3 минут\n\n"
            "<b>Форма оплачена {status}</b>".format(
                status='Да' if payment_is_completed else 'Нет'
            )
        ),
        reply_markup=await payments_keyboard("unban", url=payment_form.link_for_customer)
    )
    if payment_is_completed:
        await db_commands.update_user_data(telegram_id=call.from_user.id, is_banned=False)


@dp.callback_query_handler(state='payment', text='cancel_payment')
async def cancel_payment(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer(cache_time=60)
    await call.message.edit_text(_("Вы забанены!"), reply_markup=await unban_user_keyboard())
    await state.reset_state()


@dp.callback_query_handler(text="check_price")
async def check_price(call: CallbackQuery) -> None:
    await bot.answer_callback_query(call.id, text=_("✔️ Цена актуальна"))
