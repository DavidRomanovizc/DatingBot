from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import ADMINS
from utils.db_api import db_commands


class IsMaintenance(BaseMiddleware):

    def __init__(self):
        super(IsMaintenance, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        setting = await db_commands.select_setting()
        try:
            if setting.get('is_maintenance') and message.from_user.id not in ADMINS:
                await message.answer('Ведутся технические работы!!!')
                raise BaseException
        except Exception as err:
            pass
