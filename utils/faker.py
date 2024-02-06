from datetime import (
    datetime,
    timedelta,
)
import random

import psycopg2

from data.config import (
    load_config,
)

db_params = {
    "host": load_config().db.host,
    "database": load_config().db.database,
    "user": load_config().db.user,
    "password": load_config().db.password,
}

cities = ["cities"]
photos = [
    "id of photos"
]


def create_users(num_users):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    for _ in range(num_users):
        user_data = {
            "created_at": datetime.now() - timedelta(days=random.randint(0, 365 * 5)),
            "updated_at": datetime.now() - timedelta(days=random.randint(0, 365 * 5)),
            "telegram_id": random.randint(10_000_000, 100_000_000),
            "name": "User" + str(random.randint(1, 10000)),
            "username": "user" + str(random.randint(1, 10000)),
            "sex": random.choice(["Женский", "Мужской"]),
            "age": random.randint(18, 80),
            "city": random.choice(cities),
            "need_city": random.choice(cities),
            "longitude": random.uniform(-180, 180),
            "latitude": random.uniform(-90, 90),
            "verification": random.choice([True, False]),
            "language": "en" if random.random() < 0.5 else "es",
            "varname": "Var" + str(random.randint(1, 100)),
            "lifestyle": None,
            "is_banned": random.choice([True, False]),
            "photo_id": random.choice(photos),
            "commentary": "Comment" + str(random.randint(1, 100)),
            "need_partner_sex": random.choice(["Мужской", "Женский"]),
            "need_partner_age_min": random.randint(18, 80),
            "need_partner_age_max": random.randint(18, 80),
            "phone_number": None,
            "status": True,
            "instagram": "insta_" + str(random.randint(1, 10000)),
        }

        insert_query = """
        INSERT INTO usersmanage_user (
            telegram_id, name, username, sex, age, city, need_city,
            longitude, latitude, verification, language, varname, lifestyle,
            is_banned, photo_id, commentary, need_partner_sex, need_partner_age_min,
            need_partner_age_max, phone_number, status, instagram, created_at, updated_at
        )
        VALUES (
            %(telegram_id)s, %(name)s, %(username)s, %(sex)s, %(age)s, %(city)s,
            %(need_city)s, %(longitude)s, %(latitude)s, %(verification)s, %(language)s,
            %(varname)s, %(lifestyle)s, %(is_banned)s, %(photo_id)s, %(commentary)s,
            %(need_partner_sex)s, %(need_partner_age_min)s, %(need_partner_age_max)s,
            %(phone_number)s, %(status)s, %(instagram)s, %(created_at)s, %(updated_at)s
        )
        """

        cursor.execute(insert_query, user_data)
        conn.commit()

    cursor.close()
    conn.close()


num_users_to_create = 500_000
create_users(num_users_to_create)
