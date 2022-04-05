import asyncio

from aiogram import types
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from loguru import logger

from handlers.users.back_handler import delete_message
from keyboards.default.get_contact_inline import contact_keyboard
from keyboards.inline.second_menu_inline import second_menu_keyboard
from loader import dp
from utils.db_api import db_commands


@dp.callback_query_handler(text="verification")
async def get_verification_status(call: CallbackQuery):
    await delete_message(call.message)
    await call.message.answer("Чтобы пройти верификацию вам нужно отправить свой контакт",
                              reply_markup=await contact_keyboard())


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    contact = message.contact
    telegram_id = message.from_user.id
    user = await db_commands.select_user(telegram_id=telegram_id)

    user_verification = user.get('verification')
    if user_verification:
        user_verification = '✅ Подтвержденный'
    else:
        user_verification = '❌ Неподтвержденный'

    if contact:
        await db_commands.update_user_data(verification=True, telegram_id=telegram_id)
        await db_commands.update_user_data(phone_number=contact.phone_number, telegram_id=telegram_id)
        await message.answer(f"Спасибо, {contact.full_name}.\n"
                             f"Ваш номер {contact.phone_number} был получен.\nСтатус вашей: {user_verification}",
                             reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(4)
        await delete_message(message)
        await message.answer("Вы были возвращены в меню", reply_markup=await second_menu_keyboard())
    else:
        await db_commands.update_user_data(verification=False, telegram_id=telegram_id)
        await message.answer("Ваш номер недейственен, попробуйте еще раз.")
