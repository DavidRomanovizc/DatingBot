import uuid

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import load_config
from keyboards.inline.admin_inline import unban_user_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.payments_inline import payments_keyboard
from loader import dp, bot, _, wallet
from utils.db_api import db_commands
from utils.yoomoney.types import PaymentSource


@dp.callback_query_handler(text="unban")
async def get_payment(call: CallbackQuery, state: FSMContext) -> None:
    payment_form = await wallet.create_payment_form(
        amount_rub=2,
        unique_label=uuid.uuid4().hex,
        payment_source=PaymentSource.YOOMONEY_WALLET,
        success_redirect_url=load_config().misc.redirect_url,
    )

    await call.message.edit_text(
        text=_(
            "<b>💳 Стоимость разбана - 600</b>\n"
            "├Чтобы проверить актуальность цен, нажмите на кнопку \n"
            "├Оплата обычно приходить в течение 1-3 минут\n\n"
        ),
        reply_markup=await payments_keyboard(url=payment_form.link_for_customer)
    )

    await state.set_state("payment")
    await state.update_data(
        {
            "label": payment_form.payment_label,
            "form": payment_form.link_for_customer
        }
    )


@dp.callback_query_handler(text="check_payment", state="payment")
async def check_payment(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    payment_is_completed: bool = await wallet.check_payment_on_successful(label=data.get("label"))
    markup = await start_keyboard(obj=call)
    if payment_is_completed:
        await call.message.edit_text(
            text=_(
                "Поздравляем! Вы были разрабанены"
            ),
            reply_markup=markup
        )
        await db_commands.update_user_data(telegram_id=call.from_user.id, is_banned=False)
        await state.reset_state()
    else:
        await call.message.edit_text(
            text=_(
                "Оплата не прошла! Подождите минут 10, а затем еще раз попробуйте нажать кнопку ниже"
            ),
            reply_markup=await payments_keyboard(url=data.get("form"))
        )


@dp.callback_query_handler(state='payment', text='unban_menu')
async def cancel_payment(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(_("Вы забанены!"), reply_markup=await unban_user_keyboard())
    await state.reset_state()


@dp.callback_query_handler(text="check_price")
async def check_price(call: CallbackQuery) -> None:
    await bot.answer_callback_query(call.id, text=_("✔️ Цена актуальна"))
