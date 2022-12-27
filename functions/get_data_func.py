from typing import Tuple

from utils.db_api import db_commands
from utils.db_api.db_commands import select_user_meetings


async def get_data(telegram_id: int) -> Tuple[str, int, str, str, str, str, str, str, str, str, str, str, str]:
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_name = user.get("varname")
    user_age = user.get("age")
    user_sex = user.get("sex")
    user_city = user.get("city")
    user_need_city = user.get("need_city")
    user_life_style = user.get("lifestyle")
    user_voice_comm = user.get("voice_id")
    user_comm = user.get("commentary")
    user_verification = user.get("verification")
    photo_random_user = user.get("photo_id")
    user_inst = user.get("instagram")
    user_status = user.get("status")
    user_need_gender = user.get("need_partner_sex")

    if user_inst is None:
        user_inst = "Пользователь не прикрепил Instagram"
    if photo_random_user is None:
        photo_random_user = "https://www.meme-arsenal.com/memes/5eae5104f379baa355e031fa1ded886c.jpg"
    if user_verification:
        user_verification = '✅'
    else:
        user_verification = '❌'
    if user_name is None:
        user_name = "Не определено"
    if user_sex is None:
        user_sex = "Не определен"
    if user_city is None:
        user_city = "Не определен"
    if user_life_style is None:
        user_life_style = "Не определен"
    if user_comm is None:
        user_comm = "Пусто"

    return (
        user_name, user_age, user_sex, user_city,
        user_life_style, user_comm, user_verification, photo_random_user, user_inst, user_status, user_need_gender,
        user_voice_comm, user_need_city
    )


async def get_data_meetings(telegram_id: int) -> Tuple[str, str, str, str, str, str, str, bool, bool, bool, bool]:
    user = await select_user_meetings(telegram_id=telegram_id)
    username = user.get("username")
    verification_status = user.get("verification_status")
    is_premium = user.get("is_premium")
    is_moderation = user.get("moderation_process")
    event_name = user.get("event_name")
    commentary = user.get("commentary")
    time_event = user.get("time_event")
    venue = user.get("venue")
    photo_id = user.get("photo_id")
    is_admin = user.get("is_admin")
    is_active = user.get("is_active")

    if verification_status:
        verification_status = "Одобрено"
    else:
        verification_status = "Не одобрено"

    return (
        username,
        commentary, event_name, time_event, venue, photo_id, verification_status, is_premium, is_moderation, is_active,
        is_admin
    )
