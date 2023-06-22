import asyncio

from aiogram import types
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from handlers.users.back_handler import delete_message
from keyboards.default.get_contact_default import contact_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp, _
from utils.db_api import db_commands


@dp.callback_query_handler(text="verification")
async def get_verification_status(call: CallbackQuery) -> None:
    await delete_message(call.message)
    await call.message.answer(_("Чтобы пройти верификацию вам нужно отправить свой контакт"),
                              reply_markup=await contact_keyboard())


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message) -> None:
    contact = message.contact
    telegram_id = message.from_user.id
    user_db = await db_commands.select_user(telegram_id=telegram_id)
    if contact:
        await db_commands.update_user_data(verification=True, telegram_id=telegram_id)
        await db_commands.update_user_data(phone_number=contact.phone_number, telegram_id=telegram_id)
        await asyncio.sleep(2)
        await message.answer(_("Спасибо, {contact_full_name}.\n"
                               "Ваш номер {contact_phone_number} был получен.")
                             .format(contact_full_name=contact.full_name, contact_phone_number=contact.phone_number),
                             reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(4)
        await delete_message(message)
        await message.answer(_("Вы были возвращены в меню"),
                             reply_markup=await start_keyboard(status=user_db['status']))
    else:
        await db_commands.update_user_data(verification=False, telegram_id=telegram_id)
        await message.answer(_("Ваш номер недействителен, попробуйте еще раз."))
