from typing import Union

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import load_config
from utils.db_api import db_commands


class IsMaintenance(BaseMiddleware):

    def __init__(self):
        super(IsMaintenance, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        try:

            await self.check_tech_works(message)
        except AttributeError:
            pass

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        try:
            await self.check_tech_works(call)
        except AttributeError:
            pass

    async def check_tech_works(self, message: Union[None, types.Message] = None,
                               call: Union[None, types.CallbackQuery] = None):
        setting = await db_commands.select_setting_tech_work()

        if call and setting.get("technical_works") and call.from_user.id not in load_config().tg_bot.admin_ids:
            await call.answer("Ведутся технические работы!!!", show_alert=True)
            raise CancelHandler()
        else:
            pass
        if message:
            if setting.get("technical_works") and message.from_user.id not in load_config().tg_bot.admin_ids:
                await message.answer("Ведутся технические работы!!!")
                raise CancelHandler()
