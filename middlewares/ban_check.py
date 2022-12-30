from typing import Union

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

from functions.get_data_func import get_data
from keyboards.inline.admin_inline import unban_user_keyboard
from utils.db_api import db_commands
from aiogram import types
from loader import _


class BanMiddleware(BaseMiddleware):

    def __init__(self):
        super(BanMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        await self.check_ban_user(message)

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        await self.check_ban_user(call)

    async def check_ban_user(self, message: Union[None, types.Message] = None,
                             call: Union[None, types.CallbackQuery] = None):
        try:
            if call:
                user = await get_data(telegram_id=call.from_user.id)
                is_banned = user[13]
                if is_banned:
                    await call.message.answer(_("Вы забанены!"), reply_markup=await unban_user_keyboard())
                    raise CancelHandler()
            if message:
                user = await db_commands.select_user(telegram_id=message.from_user.id)
                is_banned = user.get("is_banned")

                if is_banned:
                    await message.answer(_("Вы забанены!"), reply_markup=await unban_user_keyboard())
                    raise CancelHandler()
        except Exception:
            raise CancelHandler()
