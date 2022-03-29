from aiogram.types import CallbackQuery

from keyboards.inline.filters_inline import filters_keyboard, filters_data_kb
from loader import dp


@dp.callback_query_handler(text="filters")
async def get_filters(call: CallbackQuery):
    markup = await filters_keyboard()
    await call.message.edit_text("Выберите фильтр: ", reply_markup=markup)


@dp.callback_query_handler(filters_data_kb.filter())
async def filters_change(call: CallbackQuery):
    print(f"ХАХАХА ПРИКОЛ {call.data}")
