import asyncio

from aiogram.types import CallbackQuery

from data.config import load_config
from functions.main_app.get_data_func import get_data_meetings
from keyboards.inline.poster_inline import poster_keyboard
from loader import dp, bot, _
from utils.db_api import db_commands


@dp.callback_query_handler(lambda call: str(call.message.chat.id) == load_config().tg_bot.moderate_chat)
async def order_answer(call: CallbackQuery):
    call_data = call.data.split("-")
    user = await get_data_meetings(call.from_user.id)
    is_admin = user[10]
    is_verification = user[6]

    if call_data[0] == 'moderate_accept':
        await call.message.delete()
        await call.message.answer(_("Принято!"))
        await db_commands.update_user_meetings_data(telegram_id=call_data[1], verification_status=True)
        await db_commands.update_user_meetings_data(telegram_id=call_data[1], is_admin=True)
        await bot.send_message(chat_id=call_data[1], text="Ваше мероприятие прошло модерацию",
                               reply_markup=await poster_keyboard(is_admin, is_verification))
        await asyncio.sleep(30)

    elif call_data[0] == 'moderate_decline':
        await call.message.delete()
        await call.message.answer("Отклонено!")
        await db_commands.delete_user_meetings(telegram_id=call_data[1])
        await bot.send_message(chat_id=call_data[1], text="К сожалению ваше мероприятие не прошло модерацию",
                               reply_markup=await poster_keyboard(is_admin, is_verification))
    await db_commands.update_user_meetings_data(telegram_id=call_data[1], moderation_process=True)
