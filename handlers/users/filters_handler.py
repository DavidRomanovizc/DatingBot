from aiogram.types import CallbackQuery

from keyboards.inline.filters_button import filters_keyboard
from loader import dp


@dp.callback_query_handler(text="filters")
async def get_filters(call: CallbackQuery):
    markup = await filters_keyboard()
    await call.message.edit_text("Выберите фильтр: ", reply_markup=markup)


