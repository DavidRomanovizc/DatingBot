from keyboards.inline.main_menu import inline_start
from keyboards.inline.second_menu import menu_inline_kb
from aiogram.types import CallbackQuery
from loader import dp, bot, db


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    await call.message.edit_text("<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств\n\n"
                                 "<b>🤝 Сотрудничество: </b>\n"
                                 "Если у вас есть предложение о сотрудничестве, пишите сюда - "
                                 "@DRomanovizc", reply_markup=inline_start)


@dp.callback_query_handler(text="submenu")
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text("<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств\n\n"
                                 "<b>🤝 Сотрудничество: </b>\n"
                                 "Если у вас есть предложение о сотрудничестве, пишите сюда - "
                                 "@DRomanovizc", reply_markup=inline_start)


@dp.callback_query_handler(text="go_bac_to_second_menu")
async def back_second_menu(call: CallbackQuery):
    await call.message.edit_text("Вы были возвращены в меню: ", reply_markup=menu_inline_kb)


@dp.callback_query_handler(text="close_everything")
async def get_close_everything(call: CallbackQuery):
    count_users = await db.count_users()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer("<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                              "<b>🤝 Сотрудничество: </b>\n"
                              "Если у вас есть предложение о сотрудничестве, пишите сюда - "
                              "@DRomanovizc", reply_markup=inline_start)
