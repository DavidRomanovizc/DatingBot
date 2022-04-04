from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType

from keyboards.inline.lifestyle_choice_inline import lifestyle_keyboard
from keyboards.inline.registration_inline import gender_keyboard, education_keyboard, town_keyboard, car_keyboard, \
    hobbies_keyboard, family_keyboard
from keyboards.inline.second_menu_inline import second_menu_keyboard
from keyboards.inline.profile_inline import registration_keyboard
from keyboards.inline.gender_inline import gender_partner_keyboard

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
    if call.data == 'male_reg':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex="Мужской")
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'female_reg':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex='Женский')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)

    await call.message.edit_text(f'Теперь напишите немного о себе: \n\n(255 символов max.)')
    await RegData.commentary.set()


@dp.message_handler(state=RegData.commentary)
async def commentary_reg(message: types.Message):
    markup = await gender_partner_keyboard()
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
    if call.data == 'gen_male':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, need_partner_sex='Мужской')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'g_fe':
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
    await message.answer("Введите вашу национальность:")
    await RegData.nationality.set()


@dp.message_handler(state=RegData.nationality)
async def get_nationality(message: types.Message, state: FSMContext):
    markup = await education_keyboard()
    await state.update_data(nationality=message.text)
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, national=message.text)
        await state.update_data(nationality=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Введите ваше образование:", reply_markup=markup)
    await RegData.education.set()


@dp.callback_query_handler(state=RegData.education)
async def get_education(call: CallbackQuery, state=FSMContext):
    if call.data == 'higher_edu':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, education='Высшее')
            await state.update_data(education='Высшее')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'secondary_edu':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, education='Среднее')
            await state.update_data(education="Среднее")
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    await call.message.edit_text(text="Введите город в котором проживаете:")
    await RegData.town.set()


@dp.message_handler(state=RegData.town)
async def get_town(message: types.Message, state: FSMContext):
    markup = await town_keyboard()
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, city=message.text)
        await state.update_data(town=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Имеете ли вы машину:", reply_markup=markup)
    await RegData.car.set()


@dp.callback_query_handler(state=RegData.car)
async def get_car(call: CallbackQuery, state: FSMContext):
    markup = await car_keyboard()
    if call.data == 'car_true':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, car=True)
            await state.update_data(car='Есть машина')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'car_false':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, car=False)
            await state.update_data(car='Нет машины')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    await call.message.edit_text("Имеете ли вы свое жилье:", reply_markup=markup)
    await RegData.own_home.set()


@dp.callback_query_handler(state=RegData.own_home)
async def get_own_home(call: CallbackQuery, state: FSMContext):
    markup = await lifestyle_keyboard()
    if call.data == 'apart_true':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, apartment=True)
            await state.update_data(own_home='Есть квартира')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'apart_false':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, apartment=False)
            await state.update_data(own_home='Нет квартиры')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    await call.message.edit_text("Чем вы занимаетесь:", reply_markup=markup)
    await RegData.hobbies.set()


@dp.callback_query_handler(state=RegData.hobbies)
async def get_hobbies(call: CallbackQuery, state: FSMContext):
    markup = await hobbies_keyboard()
    if call.data == 'study_lifestyle':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, lifestyle='Учусь')
            await state.update_data(hobbies='Учусь')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'work_lifestyle':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, lifestyle='Работаю')
            await state.update_data(hobbies='Работаю')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'job_find_lifestyle':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, lifestyle='Ищу работу')
            await state.update_data(hobbies='Ищу работу')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'householder_lifestyle':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, lifestyle='Домохозяйка/Домохозяин')
            await state.update_data(hobbies='Домохозяйка/Домохозяин')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    await call.message.edit_text("Выберите ваше семейное положение", reply_markup=markup)
    await RegData.marital.set()


@dp.callback_query_handler(state=RegData.marital)
async def get_marital(call: CallbackQuery, state=FSMContext):
    markup = await family_keyboard()

    if call.data == 'busy':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, marital='Занят/a')
            await state.update_data(marital='Занят')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'not_busy':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, marital='Не занят/a')
            await state.update_data(marital='Не занят')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)

    await call.message.edit_text("Есть ли у вас дети?", reply_markup=markup)
    await RegData.child.set()


@dp.callback_query_handler(state=RegData.child)
async def get_children(call: CallbackQuery, state=FSMContext):
    if call.data == 'true':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, kids=True)
            await state.update_data(child='Есть дети')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'false':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, kids=False)
            await state.update_data(child='Нет детей')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    await call.message.edit_text(f'И напоследок, отправьте мне Вашу фотографию')
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
                                       f"Статус анкеты - {str(user_data[12])}\n\n"
                                       f"1. Ваше имя - {str(user_data[0])}\n"
                                       f"2. Ваш возраст - {str(user_data[1])}\n"
                                       f"3. Ваш пол - {str(user_data[2])}\n"
                                       f"4. Ваша национальность - {str(user_data[3])}\n"
                                       f"5. Ваше образование - {str(user_data[4])}\n"
                                       f"6. Ваш город - {str(user_data[5])}\n"
                                       f"7. Наличие машины - {str(user_data[6])}\n"
                                       f"8. Наличие жилья - {str(user_data[7])}\n"
                                       f"9. Ваше занятие - {str(user_data[8])}\n"
                                       f"10. Наличие детей - {str(user_data[9])}\n"
                                       f"11. Семейное положение - {str(user_data[10])}\n\n"
                                       f"12. О себе - {str(user_data[11])}\n\n",
                               photo=user.get('photo_id'))

    await message.answer("Меню: ", reply_markup=markup)
