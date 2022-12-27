from aiogram.types import CallbackQuery

from keyboards.inline.poster_inline import event_filters_keyboard
from loader import dp


@dp.callback_query_handler(text="event_filters")
async def choice_event_filter(call: CallbackQuery):
    await call.message.edit_text("Вы перешли в меню фильтров", reply_markup=await event_filters_keyboard())
