import logging
import os

import django
from aiogram import executor

from loader import dp, db, bot, storage
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import filters
    import middlewares
    # filters.setup(dp)
    middlewares.setup(dp)

    logging.info(f'Подключаюсь к базе данных...')
    await db.create()

    # logging.info(f'Создаю таблицу пользователей...')
    # await db.create_table_users()
    #
    # logging.info(f'Создаю таблицу платежей...')
    # await db.create_table_payments()

    logging.info(f'Готово!')

    from utils.notify_admins import on_startup_notify
    # try:
    #     db.create_table_users()
    # except Exception as e:
    #     print(e)
    # db.delete_users()
    # print(db.select_all_users())

    await on_startup_notify(dp)
    await set_default_commands(dp)


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
