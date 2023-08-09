from typing import Union, NoReturn

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import logger

from keyboards.inline.admin_inline import unban_user_keyboard
from loader import _
from utils.db_api import db_commands


class BanMiddleware(BaseMiddleware):

    def __init__(self):
        super(BanMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict) -> None:
        await self.check_ban_user(message)

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict) -> None:

        user = await db_commands.select_user(telegram_id=call.from_user.id)
        is_banned = user.get("is_banned")
        if (user is not None and is_banned) and \
                (call.data != "unban" and
                 call.data != "unban_menu" and
                 call.data != "check_price" and
                 call.data != "pay_qiwi" and
                 call.data != "check_payment" and
                 call.data != "cancel_payment"):
            await self.check_ban_user(call=call)

    async def check_ban_user(
            self,
            message: Union[None, types.Message] = None,
            call: Union[None, types.CallbackQuery] = None) -> NoReturn:

        if call:
            user = await db_commands.select_user(telegram_id=call.from_user.id)
            is_banned = user.get("is_banned")
            try:
                if is_banned:
                    await call.message.answer(
                        text=_("Вы забанены!"),
                        reply_markup=await unban_user_keyboard()
                    )
            except TypeError as err:
                logger.info(err)
                raise CancelHandler()
            raise CancelHandler()

        if message:
            try:
                user = await db_commands.select_user(telegram_id=message.from_user.id)
                is_banned = user.get("is_banned")

                if is_banned:
                    try:
                        await message.answer(
                            text=_("Вы забанены!"),
                            reply_markup=await unban_user_keyboard()
                        )
                    except TypeError as err:
                        logger.info(err)
                        raise CancelHandler()
                    raise CancelHandler()
            except AttributeError as err:
                logger.info(err)
                # await register_user(message)
