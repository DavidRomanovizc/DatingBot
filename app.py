import logging
import os
import django
from django_project.telegrambot.telegrambot import settings
from aiogram import executor

from loader import dp, db, scheduler
import filters
from utils.notify_admins import AdminNotification

from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher) -> None:
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Уведомляет о запуске
    await AdminNotification.send(dispatcher)
    logging.info(f'Создаем подключение...')
    await db.create()
    logging.info(f'Подключение успешно!')
    logging.info(f'База загружена успешно!')


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_project.telegrambot.telegrambot.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()
    import middlewares
    import handlers

    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
