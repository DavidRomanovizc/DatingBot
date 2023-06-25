import asyncio
import random
import secrets
import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from functions.dating.create_forms_funcs import create_questionnaire, create_questionnaire_reciprocity, rand_user_list
from functions.dating.get_next_user_func import get_next_user
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.questionnaires_inline import action_keyboard, action_reciprocity_keyboard
from loader import dp, _, bot
from utils.db_api import db_commands


@dp.callback_query_handler(text='find_ques')
async def start_finding(call: CallbackQuery, state: FSMContext) -> None:
    telegram_id = call.from_user.id
    user_list = await get_next_user(telegram_id, call)
    random_user = random.choice(user_list)
    await create_questionnaire(form_owner=random_user, chat_id=telegram_id)
    await state.set_state("finding")


@dp.callback_query_handler(action_keyboard.filter(action=["like", "dislike", "stopped"]),
                           state='finding')
async def like_questionnaire(call: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]) -> None:
    action = callback_data['action']
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    username = call.from_user.username
    varname = user_db.get("varname")
    if action == "like":

        text = _('Вами заинтересовался пользователь '
                 '<a href="https://t.me/{username}">{varname_0}</a>').format(username=username,
                                                                             varname_0=varname)

        target_id = callback_data["target_id"]
        await create_questionnaire(form_owner=call.from_user.id, chat_id=target_id,
                                   add_text=text)

        await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                            message_id=call.message.message_id,
                                            reply_markup=None)
        await create_questionnaire(form_owner=(await rand_user_list(call)), chat_id=call.from_user.id)

        await state.reset_data()
    elif action == "dislike":
        try:
            await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                                message_id=call.message.message_id,
                                                reply_markup=None)
            await create_questionnaire(form_owner=(await rand_user_list(call)), chat_id=call.from_user.id)
            await state.reset_data()
        except Exception as err:
            logger.error(err)
            await create_questionnaire(form_owner=(await rand_user_list(call)), chat_id=call.from_user.id)
    elif action == "stopped":
        text = _("Рад был помочь, {fullname}!\n"
                 "Надеюсь, ты нашел кого-то благодаря мне").format(fullname=call.from_user.full_name)
        await call.answer(text, show_alert=True)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                            message_id=call.message.message_id,
                                            reply_markup=await start_keyboard(user_db["status"]))

        await state.reset_state()


@dp.callback_query_handler(action_reciprocity_keyboard.filter(action=["like_reciprocity", "dislike_reciprocity"]))
async def like_questionnaire_reciprocity(call: CallbackQuery, state: FSMContext,
                                         callback_data: typing.Dict[str, str]) -> None:
    action = callback_data['action']
    username = call.from_user.username
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    varname = user_db.get("varname")
    if action == "like_reciprocity":
        user_for_like = callback_data["user_for_like"]
        user_db = await db_commands.select_user(telegram_id=call.from_user.id)
        await asyncio.sleep(1)

        await call.answer(_("Ваша анкета отправлена другому пользователю"), show_alert=True)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                            message_id=call.message.message_id,
                                            reply_markup=await start_keyboard(user_db["status"]))

        await asyncio.sleep(5)
        await create_questionnaire_reciprocity(liker=call.from_user.id, chat_id=user_for_like,
                                               add_text=f'Вам ответили взаимностью, пользователь - '
                                                        f'<a href="https://t.me/{username}">{varname}</a>')
        await state.reset_state()
    elif action == "dislike_reciprocity":
        await asyncio.sleep(1)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                            message_id=call.message.message_id,
                                            reply_markup=await start_keyboard(user_db["status"]))
        await state.reset_state()
    await state.reset_state()


@dp.callback_query_handler(state="*", text="go_back_to_viewing_ques")
async def like_questionnaire(call: CallbackQuery, state: FSMContext) -> None:
    await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        reply_markup=None)
    await asyncio.sleep(0.1)
    user_list = await get_next_user(call.from_user.id, call)
    random_user = secrets.choice(user_list)
    try:
        await create_questionnaire(form_owner=random_user, chat_id=call.from_user.id)
        await state.reset_data()
    except IndexError:
        await call.answer(_("На данный момент у нас нет подходящих анкет для вас"))
        await state.reset_data()


@dp.message_handler(state='finding')
async def echo_message_finding(message: types.Message, state: FSMContext) -> None:
    user_db = await db_commands.select_user(telegram_id=message.from_user.id)
    await message.answer(_("Меню: "), reply_markup=await start_keyboard(user_db["status"]))
    await state.reset_state()
