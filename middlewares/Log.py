from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.logger import logger


class LogMiddleware(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        logger.debug(
            {
                "user_id: ": message.from_user.id,
                "username: ": message.from_user.username,
                "message_text:": message.text
            }
        )

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        logger.debug(call)
