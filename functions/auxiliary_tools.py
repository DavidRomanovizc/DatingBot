from typing import NoReturn, Optional

import asyncpg
from aiogram import types
from aiogram.types import CallbackQuery
from loguru import logger

from functions.get_data_filters_func import get_data_filters
from functions.get_data_func import get_data

from keyboards.inline.filters_inline import filters_keyboard
from keyboards.inline.registration_inline import confirm_keyboard
from loader import client, _
from utils.db_api import db_commands


async def choice_gender(call: CallbackQuery) -> NoReturn:
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


async def determining_location(message: types.Message, flag: Optional[bool] = None, event: bool = False) -> NoReturn:
    markup = await confirm_keyboard()
    x, y = await client.coordinates(message.text)
    city = await client.address(f"{x}", f"{y}")
    text = _('Я нашел такой адрес:\n'
             '<b>{city}</b>\n'
             'Если все правильно то подтвердите').format(city=city)
    if flag:
        await message.answer(text, reply_markup=markup)
        await db_commands.update_user_data(telegram_id=message.from_user.id, city=city)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_city=city)
        await db_commands.update_user_data(telegram_id=message.from_user.id, longitude=x)
        await db_commands.update_user_data(telegram_id=message.from_user.id, latitude=y)
    # Don't remove it otherwise it will break
    elif flag == False:
        await message.answer(text, reply_markup=markup)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_city=city)

    if event:
        await message.answer(text, reply_markup=markup)
        await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, venue=city)


async def display_profile(call: CallbackQuery, markup) -> NoReturn:
    user_data = await get_data(call.from_user.id)
    text = _("{user_0}, "
             "{user_1} лет, "
             "{user_3} {user_6}\n\n"
             "{user_5}").format(user_0=str(user_data[0]), user_1=str(user_data[1]),
                                user_3=str(user_data[3]),
                                user_5=str(user_data[5]),
                                user_6=str(user_data[6]),
                                )
    text_2 = _("{user_0}, "
               "{user_1} лет, "
               "{user_3} {user_6}\n\n"
               "{user_5}\n\n"
               "<b>Инстаграм</b> - <code>{user_8}</code>\n").format(user_0=str(user_data[0]),
                                                                    user_1=str(user_data[1]),
                                                                    user_3=str(user_data[3]),
                                                                    user_5=str(user_data[5]),
                                                                    user_6=str(user_data[6]),
                                                                    user_8=str(user_data[8]))
    text_3 = _("{user_0}, "
               "{user_1} лет, "
               "{user_3} {user_6}\n\n").format(user_0=str(user_data[0]),
                                               user_1=str(user_data[1]),
                                               user_3=str(user_data[3]),
                                               user_6=str(user_data[6]))
    if user_data[11] is None and user_data[8] == "Пользователь не прикрепил Instagram":
        await call.message.answer_photo(caption=text, photo=user_data[7], reply_markup=markup)
    elif user_data[11] is None:
        await call.message.answer_photo(caption=text_2,
                                        photo=user_data[7], reply_markup=markup)
    elif user_data[11] and user_data[8] == "Пользователь не прикрепил Instagram":
        await call.message.answer_photo(caption=text_3,
                                        photo=user_data[7], reply_markup=markup)
        await call.message.answer_voice(user_data[11], caption="Описание вашей анкеты")
    else:
        await call.message.answer_photo(caption=text_2,
                                        photo=user_data[7], reply_markup=markup)
        await call.message.answer_voice(user_data[11], caption="Описание вашей анкеты")


async def show_filters(call=None, message=None):
    user_data = await get_data_filters(call.from_user.id)
    if call:
        text = _("Фильтр по подбору партнеров:\n\n"
                 "🚻 Необходимы пол партнера: {user_2}\n"
                 "🔞 Возрастной диапазон: {user_0}-{user_1} лет\n\n"
                 "🏙️ Город партнера: {user_3}").format(user_2=user_data[2], user_0=user_data[0], user_1=user_data[1],
                                                        user_3=user_data[3])
        await call.message.edit_text(text,
                                     reply_markup=await filters_keyboard())
    if message:
        text = _("Фильтр по подбору партнеров:\n\n"
                 "🚻 Необходимы пол партнера: {user_2}\n"
                 "🔞 Возрастной диапазон: {user_0}-{user_1} лет\n\n"
                 "🏙️ Город партнера: {user_3}").format(user_2=user_data[2], user_0=user_data[0], user_1=user_data[1],
                                                        user_3=user_data[3])
        await message.answer(text,
                             reply_markup=await filters_keyboard())
