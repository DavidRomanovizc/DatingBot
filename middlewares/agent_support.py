import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class SupportMiddleware(BaseMiddleware):

    @staticmethod
    async def on_pre_process_message(message: types.Message, data: dict):
        dispatcher = Dispatcher.get_current()
        state = dispatcher.current_state(chat=message.from_user.id, user=message.from_user.id)

        state_str = str(await state.get_state())
        if state_str == "in_support":
            data = await state.get_data()
            second_id = data.get("second_id")
            await message.copy_to(second_id)

            raise CancelHandler()
