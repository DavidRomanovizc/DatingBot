from aiogram.types import CallbackQuery
from keyboards.inline.registration_inline import registration_keyboard
from keyboards.inline.sponsor_inline import sponsors_keyboard
from loader import dp
from utils.db_api import db_commands
from functions.get_data_func import get_data


@dp.callback_query_handler(text="statistics")
async def get_inst(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    user_status = user_data[9]
    users_gender_M = await db_commands.count_all_users_kwarg(sex="Мужской")
    users_gender_F = await db_commands.count_all_users_kwarg(sex="Женский")
    users_city = await db_commands.count_all_users_kwarg(city="Москва")
    users_status= await db_commands.count_all_users_kwarg(status=True)
    users_verified = await db_commands.count_all_users_kwarg(verification=True)
    if user_status:
        count_users = await db_commands.count_users()
        await call.message.edit_text(f"<b>📊 Статистика: </b>\n\n"
                                     f"└Сейчас в нашем боте <b>{count_users} пользователей</b>\n"
                                     f"└Из них:\n"
                                     f"        ├<b>{users_gender_M} пользователей мужского пола</b>\n"
                                     f"        ├<b>{users_gender_F} пользователей женского пола</b>\n"
                                     f"        ├<b>{users_city} пользователей из Москвы</b>\n"
                                     f"        ├<b>{count_users - users_city} пользователей из других городов</b>\n"
                                     f"        ├<b>{users_verified} верифицированных пользователей</b>\n"
                                     f"        ├<b>{users_status} пользователей, создавшие анкету</b>\n"
                                     f"└Дата создания бота - <b>10.08.2021</b>", reply_markup=await sponsors_keyboard()
                                     )
    else:
        await call.message.edit_text("Вам необходимо зарегистрироваться, нажмите на кнопку ниже",
                                     reply_markup=await registration_keyboard())
