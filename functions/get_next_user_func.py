from typing import List

from functions.get_data_filters_func import get_data_filters
from utils.db_api import db_commands


async def get_next_user(telegram_id: int, monitoring=False) -> List[int]:
    user = await get_data_filters(telegram_id)
    if not monitoring:
        user_filter = await db_commands.search_users(user[2], user[0], user[1], user[3])
    else:
        user_filter = await db_commands.select_all_users()

    user_list = []
    for i in user_filter:
        if int(i['telegram_id']) != int(telegram_id):
            user_list.append(i['telegram_id'])
    return user_list
