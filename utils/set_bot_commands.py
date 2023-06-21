from aiogram import types


async def set_default_commands(dp) -> None:
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота")
    ])
