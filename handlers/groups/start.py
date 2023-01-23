from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from filters.FiltersChat import IsGroup
from loader import dp, _


@dp.message_handler(IsGroup(), Command("start"))
async def start_group_handler(message: Message):
    await message.answer(_("<b>Привет, я бот, проекта Que Group, для верификации анкет для знакомств</b>\n\n"))
