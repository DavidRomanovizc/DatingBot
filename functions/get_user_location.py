from utils.db_api import db_commands


async def user_location(telegram_id: int):
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_longitude = user.get("longitude")
    user_latitude = user.get("latitude")
    return user_longitude, user_latitude
