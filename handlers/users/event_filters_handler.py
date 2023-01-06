from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.poster_inline import event_filters_keyboard
from loader import dp, _


@dp.callback_query_handler(text="event_filters")
async def choice_event_filter(call: CallbackQuery):
    await call.message.edit_text(_("Вы перешли в меню фильтров для афиш"), reply_markup=await event_filters_keyboard())


@dp.callback_query_handler(text="city_event")
async def put_city_filter(call: CallbackQuery, state: FSMContext):
    ...
