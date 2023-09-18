# noinspection PyUnresolvedReferences
import logging
import os

import django
from aiogram import executor

# noinspection PyUnresolvedReferences
import filters
# noinspection PyUnresolvedReferences
from django_project.telegrambot.telegrambot import settings
# noinspection PyUnresolvedReferences
from loader import dp, db, scheduler
from utils.db_api.db_commands import reset_view_limit
from utils.logger import setup_logger
from utils.notify_admins import AdminNotification
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher) -> None:
    await set_default_commands(dispatcher)
    scheduler.add_job(
        func=reset_view_limit,
        trigger="cron",
        hour=0,
        id="reset_view_limit",
        replace_existing=True,
    )
    await AdminNotification.send(dispatcher)


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "django_project.telegrambot.telegrambot.settings"
    )
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


if __name__ == "__main__":
    setup_django()
    setup_logger("INFO", ["aiogram.bot.api"])
    # noinspection PyUnresolvedReferences
    import middlewares

    # noinspection PyUnresolvedReferences
    import handlers

    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
