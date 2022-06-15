from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.db_api import db_commands


class BanMiddleware(BaseMiddleware):

    def __init__(self):
        super(BanMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        try:
            user = await db_commands.select_user(telegram_id=message.from_user.id)
            if user.get('is_banned'):
                await message.answer('Вы забанены!')
                raise BaseException
        except Exception as err:
            pass
