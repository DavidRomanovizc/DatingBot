from aiogram import types, Dispatcher
from loguru import logger

from data.config import load_config


async def set_user_commands(dp: Dispatcher, user_id: int, commands: list[types.BotCommand]):
    try:
        await dp.bot.set_my_commands(commands,
                                     scope=types.BotCommandScopeChat(user_id))
    except Exception as ex:
        logger.error(f"{user_id}: Commands are not installed. {ex}")


async def set_default_commands(dp: Dispatcher) -> None:
    default_commands = [
        types.BotCommand("start", "🟢 Запустить бота"),
    ]

    admin_commands = [
        types.BotCommand("admin", "[Admin] ⚒ Админ-Меню"),
        types.BotCommand("users", "[Admin] 🫂 Пользователи"),
        types.BotCommand("settings", "[Admin] ⚙️ Настройки"),
        types.BotCommand("ad", "[Admin] 📊 Реклама"),
        types.BotCommand("check", "[Admin] /check [name]"),
        types.BotCommand("logs", "[Owner] 🗒 Логи")
    ]

    await dp.bot.set_my_commands(default_commands, scope=types.BotCommandScopeDefault())

    for admin_id in load_config().tg_bot.admin_ids:
        await set_user_commands(dp, admin_id, admin_commands + default_commands)
