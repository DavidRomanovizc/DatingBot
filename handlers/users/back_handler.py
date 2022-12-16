import random
from contextlib import suppress

import aiogram.utils.exceptions
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from data.config import load_config
from keyboards.inline.calendar import search_cb
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp, _
from utils.db_api import db_commands


async def delete_message(message: types.Message):
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.callback_query_handler(text="back_with_delete")
async def open_menu(call: CallbackQuery):
    heart = random.choice(['💙', '💚', '💛', '🧡', '💜', '🖤', '❤', '🤍', '💖', '💝'])
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    markup = await start_keyboard(status=user_db['status'])
    support = await db_commands.select_user(telegram_id=load_config().tg_bot.support_ids[0])
    fullname = call.from_user.full_name
    try:
        await call.message.edit_text(_("Приветствую вас, {fullname}!!\n\n"
                                       "{heart} <b> QueDateBot </b> - платформа для поиска новых знакомств.\n\n"
                                       "🪧 Новости о проекте вы можете прочитать в нашем канале - "
                                       "https://t.me/QueDateGroup \n\n"
                                       "<b>🤝 Сотрудничество: </b>\n"
                                       "Если у вас есть предложение о сотрудничестве, пишите агенту поддержки - "
                                       "@{supports}\n\n").format(fullname=fullname, heart=heart,
                                                                 supports=support['username']),
                                     reply_markup=markup)

    except aiogram.utils.exceptions.BadRequest:
        await delete_message(call.message)

        await call.message.answer(_("Приветствую вас, {fullname}!!\n\n"
                                    "{heart} <b> QueDateBot </b> - платформа для поиска новых знакомств.\n\n"
                                    "🪧 Новости о проекте вы можете прочитать в нашем канале - "
                                    "https://t.me/QueDateGroup \n\n"
                                    "<b>🤝 Сотрудничество: </b>\n"
                                    "Если у вас есть предложение о сотрудничестве, пишите агенту поддержки - "
                                    "@{supports}\n\n").format(fullname=fullname, heart=heart,
                                                              supports=support['username']),
                                  reply_markup=markup)


@dp.callback_query_handler(search_cb.filter(action="cancel"))
async def cancel_action(call: CallbackQuery):
    await open_menu(call)
