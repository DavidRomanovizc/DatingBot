from aiogram.types import CallbackQuery

from loader import dp


@dp.callback_query_handler(text="filters")
async def get_filters(call: CallbackQuery):
    await call.answer("Coming soon...")