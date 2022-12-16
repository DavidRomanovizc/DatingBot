from loader import _
from typing import List

from functions.get_data_filters_func import get_data_filters
from utils.db_api import db_commands


async def get_next_user(telegram_id: int, call, monitoring=False) -> List[int]:
    user = await get_data_filters(telegram_id)
    user_filter_2 = await db_commands.select_all_users()
    if not monitoring:
        user_filter = await db_commands.search_users(user[2], user[0], user[1], user[3])
    else:
        user_filter = await db_commands.select_all_users()

    user_list = []
    for i in user_filter:
        if int(i['telegram_id']) != int(telegram_id):
            user_list.append(i['telegram_id'])

    if len(user_list) == 0:
        await call.answer(
            _("Под ваши фильтры нет пользователей"))

        for k in user_filter_2:
            if len(user_filter) == 0 and int(k['telegram_id']) != int(telegram_id):
                user_list.append(k['telegram_id'])

    return user_list
