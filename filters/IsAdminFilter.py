from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import load_config


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in load_config().tg_bot.admin_ids
