from typing import List

from loader import _
from utils.db_api import db_commands


async def get_next_user(telegram_id: int, call, monitoring: bool = False) -> List[int]:
    user = await db_commands.select_user_object(telegram_id=telegram_id)
    viewed_profiles = user.viewed_profiles.all()

    if monitoring:
        user_filter = await db_commands.search_users_all()
    else:
        user_filter = await db_commands.search_users(
            user.need_partner_sex,
            user.need_partner_age_min,
            user.need_partner_age_max,
            user.need_city
        )

    viewed_profiles_ids = [profile.telegram_id for profile in viewed_profiles]

    user_list = []
    for i in user_filter:
        if (
                int(i['telegram_id']) != int(telegram_id) and
                i['telegram_id'] not in viewed_profiles_ids
        ):
            user_list.append(i['telegram_id'])

    if not user_list:
        await call.answer(text=_("Под ваши фильтры нет пользователей"))

        user_filter_2 = await db_commands.search_users_all()
        for k in user_filter_2:
            if (
                    k not in user_filter and
                    int(k['telegram_id']) != int(telegram_id) and
                    k['telegram_id'] not in viewed_profiles_ids
            ):
                user_list.append(k['telegram_id'])

    return user_list
