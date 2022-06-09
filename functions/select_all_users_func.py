from functions.meetings_funcs import get_meeting_data
from utils.db_api import db_commands


async def select_all_users_list(telegram_id: int):
    users_records = await db_commands.select_all_user_meetings()
    list_id = []
    for i in users_records:
        id_user = i.get('telegram_id')
        list_id.append(id_user)
    list_id.remove(telegram_id)
    for j in list_id:
        user = await get_meeting_data(j)
        if user[1] is None:
            list_id.remove(j)
    return list_id
