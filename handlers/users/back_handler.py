from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from keyboards.inline.main_menu_inline import start_keyboard
from aiogram.types import CallbackQuery
from contextlib import suppress
from aiogram import types

from keyboards.inline.second_menu_inline import second_menu_keyboard
from loader import dp


async def delete_message(message: types.Message):
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.callback_query_handler(text="back_with_delete")
async def open_menu(call: CallbackQuery):
    markup = await start_keyboard()
    await delete_message(call.message)
    await call.message.answer(f"<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                              f"<b>🤝 Сотрудничество: </b>\n"
                              f"Если у вас есть предложение о сотрудничестве, пишите сюда - "
                              f"@borisLobkov\n\n",
                              reply_markup=markup)


@dp.callback_query_handler(text="back_to_sec_menu")
async def open_second_menu(call: CallbackQuery):
    markup = await second_menu_keyboard()
    await delete_message(call.message)
    await call.message.answer(f"<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                              f"<b>🤝 Сотрудничество: </b>\n"
                              f"Если у вас есть предложение о сотрудничестве, пишите сюда - "
                              f"@borisLobkov\n\n",
                              reply_markup=markup)
