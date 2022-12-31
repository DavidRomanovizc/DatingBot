import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import re
from loguru import logger
from functions.auxiliary_tools import choice_gender, determining_location, show_filters
from keyboards.inline.change_data_profile_inline import gender_keyboard
from loader import dp, _
from utils.db_api import db_commands


# TODO: Если город партнера == None, то писать 'город неопределён'
@dp.callback_query_handler(text="filters")
async def get_filters(call: CallbackQuery):
    await show_filters(call, message=None)


@dp.callback_query_handler(text="user_age_period")
async def desired_age(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(_("Напишите минимальный возраст"))
    await state.set_state("age_period")


@dp.message_handler(state="age_period")
async def desired_min_age_state(message: types.Message, state: FSMContext):
    try:

        messages = message.text
        int_message = re.findall('[0-9]+', messages)
        int_messages = "".join(int_message)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_partner_age_min=int_messages)
        await message.answer(_("Теперь введите максимальный возраст"))
        await state.reset_state()
        await state.set_state("max_age_period")

    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла неизвестная ошибка! Попробуйте еще раз"))


@dp.message_handler(state="max_age_period")
async def desired_max_age_state(message: types.Message, state: FSMContext):
    try:
        messages = message.text
        int_message = re.findall('[0-9]+', messages)
        int_messages = "".join(int_message)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_partner_age_max=int_messages)
        await state.finish()
        await show_filters(call=None, message=message)
    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла неизвестная ошибка! Попробуйте еще раз"))


@dp.callback_query_handler(text="user_need_gender")
async def desired_max_range(call: CallbackQuery, state: FSMContext):
    markup = await gender_keyboard()
    await call.message.edit_text(_("Выберите, кого вы хотите найти:"), reply_markup=markup)
    await state.set_state("gender")


@dp.callback_query_handler(state="gender")
async def desired_gender(call: CallbackQuery, state: FSMContext):
    await choice_gender(call)
    await call.message.edit_text("Данные сохранены")
    await asyncio.sleep(1)
    await show_filters(call, message=None)
    await state.finish()


@dp.callback_query_handler(text="needs_city")
async def user_city_filter(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(_("Напишите город вашего будущего партнера"))
    await state.set_state("city")


@dp.message_handler(state="city")
async def user_city_filter_state(message: types.Message):
    try:
        await determining_location(message, flag=False)

    except Exception as err:
        logger.info(err)
        await message.answer(_("Произошла ошибка, попробуйте еще раз"))
        return


@dp.callback_query_handler(text="yes_all_good", state="city")
async def get_hobbies(call: CallbackQuery, state: FSMContext):
    await asyncio.sleep(1)
    await call.message.edit_text(_("Данные сохранены"))
    await asyncio.sleep(2)
    await show_filters(call, message=None)

    await state.finish()
