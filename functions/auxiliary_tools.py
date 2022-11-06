import asyncpg
from aiogram import types
from aiogram.types import CallbackQuery
from loguru import logger

from keyboards.inline.registration_inline import confirm_keyboard
from loader import client
from utils.db_api import db_commands


async def choice_gender(call: CallbackQuery) -> None:
    if call.data == 'male':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, need_partner_sex='Мужской')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'female':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, need_partner_sex='Женский')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)


async def determining_location(message: types.Message, flag: bool) -> None:
    if flag:
        markup = await confirm_keyboard()
        x, y = await client.coordinates(message.text)
        city = await client.address(f"{x}", f"{y}")

        await message.answer(f'Я нашел такой адрес:\n'
                             f'<b>{city}</b>\n'
                             f'Если все правильно то подтвердите.', reply_markup=markup)
        await db_commands.update_user_data(telegram_id=message.from_user.id, city=city)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_city=city)
        await db_commands.update_user_data(telegram_id=message.from_user.id, longitude=x)
        await db_commands.update_user_data(telegram_id=message.from_user.id, latitude=y)
    else:
        markup = await confirm_keyboard()
        x, y = await client.coordinates(message.text)
        city = await client.address(f"{x}", f"{y}")
        await message.answer(f'Я нашел такой адрес:\n'
                             f'<b>{city}</b>\n'
                             f'Если все правильно то подтвердите.', reply_markup=markup)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_city=city)
