from aiogram import Dispatcher

from filters.FiltersChat import IsPrivate
from loader import logger


def setup(dp: Dispatcher):
    logger.info("Подключение filters...")
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
    ]

    dp.filters_factory.bind(IsPrivate)
