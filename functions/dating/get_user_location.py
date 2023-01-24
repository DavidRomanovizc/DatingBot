import math

from utils.db_api import db_commands


async def user_location(telegram_id: int) -> tuple[float, float]:
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_longitude = user.get("longitude")
    user_latitude = user.get("latitude")
    return user_longitude, user_latitude


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return int(c * r)
