from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import load_config
from utils.db_api import db_commands


# А что это? Как оно здесь появилось и за что оно отвечает
class IsMaintenance(BaseMiddleware):

    def __init__(self):
        super(IsMaintenance, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        setting = await db_commands.select_setting()
        try:
            if setting.get('is_maintenance') and message.from_user.id not in load_config().tg_bot.admin_ids:
                await message.answer('Ведутся технические работы!!!')
                raise BaseException
        except Exception as err:
            pass
