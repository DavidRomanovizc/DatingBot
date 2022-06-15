from utils.db_api import db_commands


async def get_next_user(telegram_id, monitoring=False):
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_sex = user.get("need_partner_sex")
    user_need_age_min = user.get("need_partner_age_min")
    user_need_age_max = user.get("need_partner_age_max")
    user_need_city = user.get("need_city")
    if not monitoring:
        user_filter = await db_commands.search_users(user_sex, user_need_age_min, user_need_age_max, user_need_city)
    else:
        user_filter = await db_commands.select_all_users()

    user_list = []
    for i in user_filter:
        if int(i['telegram_id']) != int(telegram_id):
            user_list.append(i['telegram_id'])
    return user_list
