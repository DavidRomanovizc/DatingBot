import random
from contextlib import suppress

import aiogram.utils.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from data.config import load_config
from functions.main_app.app_scheduler import send_message_week
from functions.main_app.auxiliary_tools import display_profile, registration_menu
from handlers.users.event_handler import view_meetings_handler, view_own_event
from keyboards.inline.admin_inline import unban_user_keyboard
from keyboards.inline.calendar import search_cb
from keyboards.inline.filters_inline import filters_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.menu_profile_inline import get_profile_keyboard
from loader import dp, _, scheduler
from utils.db_api import db_commands


async def delete_message(message: types.Message) -> None:
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.callback_query_handler(text="back_with_delete")
async def open_menu(call: CallbackQuery) -> None:
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    heart = random.choice(['💙', '💚', '💛', '🧡', '💜', '🖤', '❤', '🤍', '💖', '💝'])
    markup = await start_keyboard(status=user_db['status'])
    support = await db_commands.select_user(telegram_id=load_config().tg_bot.support_ids[0])
    fullname = call.from_user.full_name
    text = _("Приветствую вас, {fullname}!!\n\n"
             "{heart} <b> QueDateBot </b> - платформа для поиска новых знакомств.\n\n"
             "🪧 Новости о проекте вы можете прочитать в нашем канале - "
             "https://t.me/QueDateGroup \n\n"
             "<b>🤝 Сотрудничество: </b>\n"
             "Если у вас есть предложение о сотрудничестве, пишите агенту поддержки - "
             "@{supports}\n\n").format(fullname=fullname, heart=heart,
                                       supports=support['username'])
    try:
        await call.message.edit_text(text,
                                     reply_markup=markup)

    except aiogram.utils.exceptions.BadRequest:
        await delete_message(call.message)

        await call.message.answer(text,
                                  reply_markup=markup)


@dp.callback_query_handler(text="back_to_reg_menu")
@dp.callback_query_handler(text="back_to_profile_menu")
async def event_back_handler(call: CallbackQuery) -> None:
    if call.data == "back_to_reg_menu":
        await registration_menu(call, scheduler, send_message_week, load_config, random)
    elif call.data == "back_to_profile_menu":
        telegram_id = call.from_user.id
        await delete_message(call.message)
        user_db = await db_commands.select_user(telegram_id=telegram_id)
        markup = await get_profile_keyboard(verification=user_db["verification"])
        await display_profile(call, markup)


@dp.callback_query_handler(text="unban_menu")
async def unban_back_handler(call: CallbackQuery) -> None:
    await call.message.edit_text(_("Вы забанены!"), reply_markup=await unban_user_keyboard())


@dp.callback_query_handler(search_cb.filter(action="cancel"))
async def cancel_action(call: CallbackQuery) -> None:
    await open_menu(call)


@dp.callback_query_handler(text="back_to_filter_menu")
async def back_to_filters_menu(call: CallbackQuery) -> None:
    await call.message.edit_text(_("Вы вернулись в меню фильтров"), reply_markup=await filters_keyboard())


@dp.callback_query_handler(text="go_out", state="cancel_record")
@dp.callback_query_handler(text="event_menu")
async def event_profile_back(call: CallbackQuery, state: FSMContext) -> None:
    await state.finish()
    await delete_message(call.message)
    await view_meetings_handler(call)


@dp.callback_query_handler(text="back_to_event_profile")
async def back_to_filters_menu(call: CallbackQuery) -> None:
    await view_own_event(call)
