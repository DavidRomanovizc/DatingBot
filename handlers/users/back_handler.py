from keyboards.inline.main_menu import inline_start
from keyboards.inline.second_menu import menu_inline_kb
from aiogram.types import CallbackQuery
from loader import dp


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    await call.message.edit_text(f"Рад был помочь, {call.from_user.full_name}!\n"
                                 f"Надеюсь, ты нашел кого-то благодаря мне", reply_markup=inline_start)


@dp.callback_query_handler(text="submenu")
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text("Вы были возвращены в меню: ", reply_markup=inline_start)


@dp.callback_query_handler(text="go_bac_to_second_menu")
async def back_second_menu(call: CallbackQuery):
    await call.message.edit_text("Вы были возвращены в меню: ", reply_markup=menu_inline_kb)
