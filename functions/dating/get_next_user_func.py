from typing import List

from loader import _
from utils.db_api import db_commands


async def get_next_user(telegram_id: int, call, monitoring: bool = False) -> List[int]:
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_filter = await db_commands.search_users_all() if monitoring else await db_commands.search_users(
        user.get("need_partner_sex"),
        user.get("need_partner_age_min"),
        user.get("need_partner_age_max"),
        user.get("need_city")
    )

    user_list = [i['telegram_id'] for i in user_filter if int(i['telegram_id']) != int(telegram_id)]

    if not user_list:
        await call.answer(_("Под ваши фильтры нет пользователей"))

        user_filter_2 = await db_commands.search_users_all()
        user_list = [k['telegram_id'] for k in user_filter_2 if
                     k not in user_filter and int(k['telegram_id']) != int(telegram_id)]

    return user_list
