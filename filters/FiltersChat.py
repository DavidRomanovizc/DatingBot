from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class IsPrivate(BoundFilter):
    async def check(self, message: Message) -> bool:
        return types.ChatType.PRIVATE == message.chat.type


class IsGroup(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP)
