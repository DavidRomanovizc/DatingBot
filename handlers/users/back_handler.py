from aiogram.types import CallbackQuery

from keyboards.inline.second_menu import menu_inline_kb
from loader import dp


@dp.callback_query_handler(text="back_with_delete")
async def open_menu(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(f"Меню: ",
                              reply_markup=menu_inline_kb)


