from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType

from keyboards.inline.change_inline import gender_keyboard
from keyboards.inline.second_menu_inline import second_menu_keyboard
from keyboards.inline.profile_inline import registration_keyboard


from utils.misc.create_questionnaire import get_data
from utils.db_api import db_commands

from states.reg_state import RegData

from loguru import logger
from loader import dp
import asyncpg


@dp.callback_query_handler(text='registration')
async def registration(call: CallbackQuery):
    markup = await registration_keyboard()
    text = f"Пройдите опрос, чтобы зарегистрироваться"
    await call.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(text_contains="survey")
async def survey(call: CallbackQuery):
    markup = await gender_keyboard()

    await call.message.edit_text("Выберите пол", reply_markup=markup)
    await RegData.sex.set()


@dp.callback_query_handler(state=RegData.sex)
async def sex_reg(call: CallbackQuery):
    if call.data == 'male':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex="Мужской")
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'female':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex='Женский')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)

    await call.message.edit_text(f'Теперь напишите немного о себе: \n\n(255 символов max.)')
    await RegData.commentary.set()


@dp.message_handler(state=RegData.commentary)
async def commentary_reg(message: types.Message):
    markup = await gender_keyboard()
    try:
        await db_commands.update_user_data(commentary=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Комментарий принят! Выберите, кого вы хотите найти: ', reply_markup=markup)
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка! Попробуйте изменить комментарий позже в разделе '
                             f'"Меню"\n\n'
                             f'Выберите, кого вы хотите найти: ', reply_markup=markup)
    await RegData.need_partner_sex.set()


@dp.callback_query_handler(state=RegData.need_partner_sex)
async def sex_reg(call: CallbackQuery):
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

    await call.message.edit_text(f'Отлично! Теперь напишите мне ваше имя, которое будут все видеть в анкете')
    await RegData.name.set()


@dp.message_handler(state=RegData.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, varname=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Введите сколько вам лет:")
    await RegData.age.set()


@dp.message_handler(state=RegData.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, age=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer(text="Введите город в котором проживаете:")
    await RegData.town.set()


@dp.message_handler(state=RegData.town)
async def get_town(message: types.Message, state: FSMContext):
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, city=message.text)
        await state.update_data(town=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Чем вы занимаетесь:")
    await RegData.hobbies.set()


@dp.message_handler(state=RegData.hobbies)
async def get_hobbies(message: types.Message, state: FSMContext):
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, lifestyle=message.text)
        await state.update_data(hobbies=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer(f'И напоследок, отправьте мне Вашу фотографию')
    await RegData.photo.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=RegData.photo)
async def get_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    markup = await second_menu_keyboard()
    try:
        await db_commands.update_user_data(photo_id=file_id, telegram_id=message.from_user.id)
        await message.answer(f'Фото принято!')
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n'
                             f'Если ошибка осталась, напишите системному администратору.')

    await state.finish()

    telegram_id = message.from_user.id
    user_data = await get_data(telegram_id)
    user = await db_commands.select_user(telegram_id=telegram_id)
    await message.answer_photo(caption=f"Регистрация завершена успешно! \n\n "
                                       f"<b>Статус анкеты</b> - \n{str(user_data[6])}\n\n"
                                       f"<b>Имя</b> - {str(user_data[0])}\n"
                                       f"<b>Возраст</b> - {str(user_data[1])}\n"
                                       f"<b>Пол</b> - {str(user_data[2])}\n"
                                       f"<b>Город</b> - {str(user_data[3])}\n"
                                       f"<b>Ваше занятие</b> - {str(user_data[4])}\n"
                                       f"<b>О себе</b> - {str(user_data[5])}\n\n",
                               photo=user.get('photo_id'))

    await message.answer("Меню: ", reply_markup=markup)
