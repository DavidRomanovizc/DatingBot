from aiogram.types import CallbackQuery

from keyboards.inline.back_inline import only_back_keyboard
from keyboards.inline.registration_inline import registration_keyboard
from loader import dp
from utils.db_api import db_commands
from functions.get_data_func import get_data


@dp.callback_query_handler(text="statistics")
async def get_inst(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    user_status = user_data[9]
    if user_status:
        markup = await only_back_keyboard()
        count_users = await db_commands.count_users()
        await call.message.edit_text(f"<b>💻 Статистика: </b>\n\n"
                                     f"└Сейчас в нашем боте <b>{count_users}"
                                     f" пользователей</b>\n"
                                     f"└Дата создания бота - <b>10.08.2021</b>", reply_markup=markup
                                     )
    else:
        await call.message.edit_text("Вам необходимо зарегистрироваться, нажмите на кнопку ниже",
                                     reply_markup=await registration_keyboard())
