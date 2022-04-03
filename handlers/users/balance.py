from aiogram.types import CallbackQuery

from loader import dp


@dp.callback_query_handler(text="balance")
async def deposit_balance(call: CallbackQuery):
    await call.answer("Coming soon...")
