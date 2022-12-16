import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from functions.get_data_func import get_data_meetings
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.sending_quest import moderate_keyboard, moderate_callback, cancel_moderate_callback
from keyboards.inline.support_inline import check_support_available, get_support_manager
from loader import dp, bot, _
from utils.db_api import db_commands


# TODO: Нужно сделать так, чтобы пользователь, безуспешно прошедший верификацию, смог повторить только через день
#  Нужно добавить колонку в бд либо счетчик отправок анкет, либо флаг
@dp.callback_query_handler(moderate_callback.filter(messages="many", as_user="yes"))
async def send_to_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text(_("Ваша заявка успешно отправлена! <b>Ожидайте</b>\n"
                                 "Во время модерации вашей анкеты не отправляйте ничего боту"))

    user_id = int(callback_data.get("user_id"))
    if not await check_support_available(user_id):
        support_id = await get_support_manager()
    else:
        support_id = user_id

    await state.set_state("wait_in_support")
    await state.update_data(second_id=support_id)

    keyboard = await moderate_keyboard(messages="many", user_id=call.from_user.id)
    user = await get_data_meetings(telegram_id=call.from_user.id)
    text = (
        f"Имя: @{user[0]}\n"
        f"Уровень игры: {user[3]}\n"
        f"Должность: {user[2]}\n"
        f"Компания: {user[1]}\n"

    )
    await bot.send_message(
        support_id,
        text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(moderate_callback.filter(messages="many", as_user="no"))
async def answer_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    second_id = int(callback_data.get("user_id"))
    user_state = dp.current_state(user=second_id, chat=second_id)

    if str(await user_state.get_state()) != "wait_in_support":
        await call.message.edit_text("К сожалению, пользователь уже передумал.")
        return

    await state.update_data(second_id=second_id)
    await call.message.edit_text("Анкета одобрена")
    await db_commands.update_user_meetings_data(telegram_id=second_id, verification_status=True)
    user = await get_data_meetings(telegram_id=call.from_user.id)
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    markup = await start_keyboard(status=user_db['status'])
    if user[4]:
        await bot.send_message(second_id,
                               "<b>Ваша анкета прошла модерацию</b>\n"
                               f"Ваш статус обновлен\n"
                               f"Нажмите на кнопку <b>информация</b>", reply_markup=markup)
        await state.finish()
    await state.finish()


@dp.message_handler(state="wait_in_support", content_types=types.ContentTypes.ANY)
async def not_supported(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    await state.finish()


@dp.callback_query_handler(cancel_moderate_callback.filter(), state=["in_support", "wait_in_support", None])
async def exit_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = int(callback_data.get("user_id"))
    second_state = dp.current_state(user=user_id, chat=user_id)
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    markup = await start_keyboard(status=user_db['status'])
    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get("second_id")
        if int(second_id) == call.from_user.id:
            await second_state.reset_state()
            await bot.send_message(user_id, "Ваша анкета была отклонена", reply_markup=markup)

    await call.message.edit_text("Вы завершили сеанс")
    await asyncio.sleep(2)
    await call.message.delete()
    await state.reset_state()
