from aiogram.types import CallbackQuery

from loader import dp


@dp.callback_query_handler(text="verification")
async def get_verification_status(call: CallbackQuery):
    await call.answer("Coming soon...")
