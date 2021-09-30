from keyboards.inline.BN_report import questionnaires_report_inline_kb
from utils.misc.ds_name import get_display_name
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from states.Reports import Report
from data.config import ADMINS
from aiogram import types
from loader import dp, bot


# TODO: Доделать репорты
# FIXME: Почините

# @dp.callback_query_handler(text="report") #пока не робит
async def report_user(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer("<b>Временно не работает</b>\n"
                              "Укажите причину жалобы\n"
                              "\n"
                              "1. 🔞 Материал для взрослых.\n"
                              "2. 💊 Пропаганда наркотиков.\n"
                              "3. 💰 Продажа товаров и услуг."
                              "4. 🦨 Другое.\n"
                              "\n"
                              "5. Вернуться назад.", reply_markup=questionnaires_report_inline_kb)
    await Report.first()


@dp.callback_query_handler(text="eighteen_plus_content", state=Report.first)
async def report_user(call: CallbackQuery, message: types.Message, state: FSMContext):
    await call.answer(cache_time=60)
    display_name = get_display_name(message.reply_to_message.from_user)

    await call.answer(
        f"Репорт на пользователя {display_name} успешно отправлен.\n"
        "Администрация предпримет все необходимые меры"
    )

    for admin_id in ADMINS:
        await bot.send_message(
            admin_id,
            f"Кинут репорт на пользователя {display_name} "
        )
    async with state.proxy() as data:
        data["report_us"] = display_name


@dp.callback_query_handler(text="cancel_3")
async def cancel_3(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer(f"Отмена")
    await call.message.edit_reply_markup(reply_markup=None)