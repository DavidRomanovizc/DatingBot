from aiogram.types import CallbackQuery

from functions.main_app.get_data_func import get_data
from keyboards.inline.sponsor_inline import sponsors_keyboard
from loader import dp, _
from utils.db_api import db_commands


@dp.callback_query_handler(text="statistics")
async def get_inst(call: CallbackQuery):
    user_data = await get_data(call.from_user.id)
    user_city = user_data[3]
    users_gender_m = await db_commands.count_all_users_kwarg(sex="Мужской")
    users_gender_f = await db_commands.count_all_users_kwarg(sex="Женский")
    users_city = await db_commands.count_all_users_kwarg(city=user_city)
    users_status = await db_commands.count_all_users_kwarg(status=True)
    users_verified = await db_commands.count_all_users_kwarg(verification=True)
    count_users = await db_commands.count_users()
    text = _("<b>📊 Статистика: </b>\n\n"
             "└Сейчас в нашем боте <b>{count_users} пользователей</b>\n"
             "└Из них:\n"
             "        ├<b>{users_gender_m} пользователей мужского пола</b>\n"
             "        ├<b>{users_gender_f} пользователей женского пола</b>\n"
             "        ├<b>{users_city} пользователей из города {user_city}</b>\n"
             "        ├<b>{cs_uy} пользователей из других городов</b>\n"
             "        ├<b>{users_verified} верифицированных пользователей</b>\n"
             "        ├<b>{users_status} пользователей, создавшие анкету</b>\n"
             "└Дата создания бота - <b>10.08.2021</b>").format(count_users=count_users,
                                                               users_gender_m=users_gender_m,
                                                               users_gender_f=users_gender_f,
                                                               users_city=users_city,
                                                               user_city=user_city,
                                                               cs_uy=count_users - users_city,
                                                               users_verified=users_verified,
                                                               users_status=users_status)

    await call.message.edit_text(text, reply_markup=await sponsors_keyboard())
