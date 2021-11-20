# мы не знаем, что это такое @mroshalom
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware


class CheckBan(BaseMiddleware):
    allowed_updates = ["callback_query", "message"]

    async def trigger(self, action, arg):
        obj, *args, data = arg

        if not any(
                update in action for update in self.allowed_updates
        ):
            return

        if not action.startswith("process_"):
            return
        handler = current_handler.get()
        if not handler:
            return

        allow = getattr(handler, "allow", False)
        if allow:
            return

        user: User = data.get("user")
        if not user.allowed:
            message = obj.message if isinstance(obj, types.CallbackQuery) else obj
            await message.reply("Доступ к боту запрещен")
            raise CancelHandler()
