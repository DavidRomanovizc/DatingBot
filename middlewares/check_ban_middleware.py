# мы не знаем, что это такое @mroshalom
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class CheckBan(BaseMiddleware):
    allowed_updates = ["callback_query", "message"]

    async def trigger(self, action, arg):
        obj, *args, data = arg

        if not any(
                update in action for update in self.allowed_updates
        ):
            return

        elif not action.startswith("process_"):
            return
        handler = current_handler.get()
        elif not handler:
            return

        allow = getattr(handler, "allow", False)
        if allow:
            return

        user: User = data.get("user")
        if not user.allowed:
            message = obj.message if isinstance(obj, types.CallbackQuery) else obj
            await message.reply("Доступ к боту запрещен")
            raise CancelHandler()
