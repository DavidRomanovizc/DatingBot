from aiogram import Dispatcher
from loguru import logger

from filters.filters_chat import IsPrivate


def setup(dp: Dispatcher):
    logger.info("Подключение filters...")
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
    ]

    dp.filters_factory.bind(IsPrivate)
