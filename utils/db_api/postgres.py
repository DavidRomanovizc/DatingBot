from typing import Union

import asyncpg

from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        email varchar(255) NULL,
        sex varchar(255) NULL, 
        age varchar(255) NULL,
        national varchar(255) NULL,
        education varchar(255) NULL, 
        city varchar(255) NULL,
        kids bool NULL,
        car bool NULL,
        apartment bool NULL, 
        marital varchar(255) NULL,
        language varchar(255) NULL,
        varname varchar(255) NULL,
        lifestyle varchar(255) NULL,
        is_banned bool NULL,
        photo_id varchar(255) NULL,
        commentary varchar(255) NULL,
        need_partner_sex varchar(255) NULL,
        likes varchar(255) NULL,
        dislikes varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_payments(self):  # создание таблицы оплаты
        sql = """
        CREATE TABLE IF NOT EXISTS Payments (
        id SERIAL PRIMARY KEY,
        is_premium bool NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user_Users(self, full_name, username, telegram_id, email, national, education, sex, city, age,
                             kids, car, apartment, marital, language, varname, lifestyle, is_banned, photo_id, commentary,
                             need_partner_sex, likes, dislikes):
        sql = '''INSERT INTO users (full_name, username, telegram_id, email, national, education, sex, city, age,
                       kids, car, apartment, marital, language, varname, lifestyle, is_banned, photo_id, commentary, 
                       need_partner_sex, likes, dislikes) 
                       VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22) returning *'''
        return await self.execute(sql, full_name, username, telegram_id, email, national, education, sex, city, age,
                                  kids, car, apartment, marital, language, varname, lifestyle, is_banned, photo_id,
                                  commentary, need_partner_sex, likes, dislikes,
                                  fetchrow=True)

    async def add_user_Payments(self, telegram_id, is_premium):
        sql = '''INSERT INTO users (telegram_id, is_premium) VALUES($1, $2) returning *'''
        return await self.execute(sql, telegram_id, is_premium, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_users_id(self):
        sql = "SELECT telegram_id FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_user_email(self, email, telegram_id):
        sql = "UPDATE Users SET email=$1 WHERE telegram_id=$2"
        return await self.execute(sql, email, telegram_id, execute=True)

    async def update_user_sex(self, sex, telegram_id):
        sql = "UPDATE Users SET sex=$1 WHERE telegram_id=$2"
        return await self.execute(sql, sex, telegram_id, execute=True)

    async def update_user_is_premium(self, is_premium, telegram_id):
        sql = "UPDATE Payments SET is_premium=$1 WHERE telegram_id=$2"
        return await self.execute(sql, is_premium, telegram_id, execute=True)

    async def update_user_age(self, age, telegram_id):
        sql = "UPDATE Users SET age=$1 WHERE telegram_id=$2"
        return await self.execute(sql, age, telegram_id, execute=True)

    async def update_user_national(self, national, telegram_id):
        sql = "UPDATE Users SET national=$1 WHERE telegram_id=$2"
        return await self.execute(sql, national, telegram_id, execute=True)

    async def update_user_education(self, education, telegram_id):
        sql = "UPDATE Users SET education=$1 WHERE telegram_id=$2"
        return await self.execute(sql, education, telegram_id, execute=True)

    async def update_user_city(self, city, telegram_id):
        sql = "UPDATE Users SET city=$1 WHERE telegram_id=$2"
        return await self.execute(sql, city, telegram_id, execute=True)

    async def update_user_language(self, language, telegram_id):
        sql = "UPDATE Users SET language=$1 WHERE telegram_id=$2"
        return await self.execute(sql, language, telegram_id, execute=True)

    async def update_user_marital(self, marital, telegram_id):
        sql = "UPDATE Users SET marital=$1 WHERE telegram_id=$2"
        return await self.execute(sql, marital, telegram_id, execute=True)

    async def update_user_car(self, car, telegram_id):
        sql = "UPDATE Users SET car=$1 WHERE telegram_id=$2"
        return await self.execute(sql, car, telegram_id, execute=True)

    async def update_user_apartment(self, apartment, telegram_id):
        sql = "UPDATE Users SET apartment=$1 WHERE telegram_id=$2"
        return await self.execute(sql, apartment, telegram_id, execute=True)

    async def update_user_kids(self, kids, telegram_id):
        sql = "UPDATE Users SET kids=$1 WHERE telegram_id=$2"
        return await self.execute(sql, kids, telegram_id, execute=True)

    async def update_user_varname(self, varname, telegram_id):
        sql = "UPDATE Users SET varname=$1 WHERE telegram_id=$2"
        return await self.execute(sql, varname, telegram_id, execute=True)

    async def update_user_lifestyle(self, lifestyle, telegram_id):
        sql = "UPDATE Users SET lifestyle=$1 WHERE telegram_id=$2"
        return await self.execute(sql, lifestyle, telegram_id, execute=True)

    async def update_user_ban_status(self, is_banned, telegram_id):
        sql = "UPDATE Users SET is_banned=$1 WHERE telegram_id=$2"
        return await self.execute(sql, is_banned, telegram_id, execute=True)

    async def update_user_photo_id(self, photo_id, telegram_id):
        sql = "UPDATE Users SET photo_id=$1 WHERE telegram_id=$2"
        return await self.execute(sql, photo_id, telegram_id, execute=True)

    async def update_user_commentary(self, commentary, telegram_id):
        sql = "UPDATE Users SET commentary=$1 WHERE telegram_id=$2"
        return await self.execute(sql, commentary, telegram_id, execute=True)

    async def update_user_need_partner_sex(self, need_partner_sex, telegram_id):
        sql = "UPDATE Users SET need_partner_sex=$1 WHERE telegram_id=$2"
        return await self.execute(sql, need_partner_sex, telegram_id, execute=True)

    async def update_user_likes(self, likes, telegram_id):
        sql = "UPDATE Users SET likes=$1 WHERE telegram_id=$2"
        return await self.execute(sql, likes, telegram_id, execute=True)

    async def update_user_dislikes(self, dislikes, telegram_id):
        sql = "UPDATE Users SET dislikes=$1 WHERE telegram_id=$2"
        return await self.execute(sql, dislikes, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_payments(self):
        await self.execute("DELETE FROM Payments WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def drop_payments(self):
        await self.execute("DROP TABLE Payments", execute=True)


