import asyncio

from loguru import logger

from handlers.users.back_handler import delete_message
from keyboards.inline.change_inline import gender_keyboard, car_keyboard, kids_keyboard, house_keyboard, \
    education_keyboard
from keyboards.inline.change_data_profile_inline import change_info_keyboard
from keyboards.inline.lifestyle_choice_inline import lifestyle_keyboard

from aiogram.types import CallbackQuery, ContentType, ReplyKeyboardRemove

from states.new_data_state import NewData
from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from aiogram import types

from utils.db_api import db_commands


@dp.callback_query_handler(text='change_profile')
async def start_change_data(call: CallbackQuery):
    markup = await change_info_keyboard()
    await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)


@dp.callback_query_handler(text='name')
async def change_name(call: CallbackQuery):
    await call.message.edit_text(f'Введите новое имя')
    await NewData.name.set()


@dp.message_handler(state=NewData.name)
async def change_name(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db_commands.update_user_data(varname=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Ваше новое имя: <b>{message.text}</b>')
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка',
                             reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='age')
async def change_age(call: CallbackQuery):
    await call.message.edit_text(f'Введите новый возраст')
    await NewData.age.set()


@dp.message_handler(state=NewData.age)
async def change_age(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db.update_user_age(age=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Ваш новый возраст: <b>{message.text}</b>')
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()

    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='nationality')
async def change_nationality(call: CallbackQuery):
    await call.message.edit_text(f'Введите новую национальность')
    await NewData.nationality.set()


@dp.message_handler(state=NewData.nationality)
async def change_nationality(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db.update_user_national(national=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Ваша новая национальность: <b>{message.text}</b>')
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='city')
async def change_city(call: CallbackQuery):
    await call.message.edit_text(f'Введите новый город')
    await NewData.city.set()


@dp.message_handler(state=NewData.city)
async def change_city(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db.update_user_city(city=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Ваш новый город: <b>{message.text}</b>')
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='gender')
async def change_sex(call: CallbackQuery):
    markup = await gender_keyboard()
    await call.message.edit_text(f'Выберите новый пол: ', reply_markup=markup)
    await NewData.sex.set()


@dp.callback_query_handler(state=NewData.sex)
async def change_sex(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    if call.data == 'male':
        try:
            await db.update_user_sex(sex='Мужской', telegram_id=call.from_user.id)
            await call.message.edit_text(f'Ваш новый пол: <b>Мужской</b>')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
            await state.reset_state()
    if call.data == 'female':
        try:
            await db.update_user_sex(sex='Женский', telegram_id=call.from_user.id)
            await call.message.edit_text(f'Ваш новый пол: <b>Женский</b>')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
            await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='car')
async def change_car(call: CallbackQuery):
    markup = await car_keyboard()
    await call.message.edit_text(f'Есть ли у Вас машина?: ', reply_markup=markup)
    await NewData.car.set()


@dp.callback_query_handler(state=NewData.car)
async def change_car(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    if call.data == 'true':
        try:
            await db.update_user_car(car=True, telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь у вас есть машина')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
            await state.reset_state()
    if call.data == 'false':
        try:
            await db.update_user_car(car=False, telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь у вас нет машина')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
            await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='kids')
async def change_kids(call: CallbackQuery):
    markup = await kids_keyboard()
    await call.message.edit_text(f'Есть ли у Вас дети?: ', reply_markup=markup)
    await NewData.child.set()


@dp.callback_query_handler(text='state=NewData.child')
async def change_children(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    if call.data == 'true':
        try:
            await db.update_user_kids(kids=True, telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь у вас: <b>есть</b> дети')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка', reply_markup=markup)
            await state.reset_state()
    if call.data == 'false':
        try:
            await db.update_user_kids(kids=False, telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь у вас: <b>нет</b> детей')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка. Попробуйте ещё раз', reply_markup=markup)
            await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='house')
async def change_home(call: CallbackQuery):
    markup = await house_keyboard()
    await call.message.edit_text(f'Есть ли у Вас квартира: ', reply_markup=markup)
    await NewData.own_home.set()


@dp.callback_query_handler(state=NewData.own_home)
async def change_home(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    if call.data == 'true':
        try:
            await db.update_user_apartment(apartment=True, telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь у вас: <b>есть</b> квартира')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text('Произошла неизвестная ошибка', reply_markup=markup)
            await state.reset_state()
    if call.data == 'false':
        try:
            await db.update_user_apartment(apartment=False, telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь у вас: <b>нет</b> квартиры')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка', reply_markup=markup)
            await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='education')
async def change_education(call: CallbackQuery):
    markup = await education_keyboard()
    await call.message.edit_text(f'Какое у Вас образование: ', reply_markup=markup)
    await NewData.education.set()


@dp.callback_query_handler(state=NewData.education)
async def change_education(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    if call.data == 'higher_edu':
        try:
            await db.update_user_apartment(apartment=True, telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь у вас: <b>Высшее</b> образование')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(call.from_user.id, f'Произошла неизвестная ошибка', reply_markup=markup)
            await state.reset_state()
    if call.data == 'secondary_edu':
        try:
            await db.update_user_apartment(apartment=False, telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь у вас: <b>Среднее</b> образование')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка', reply_markup=markup)
            await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='busyness')
async def change_style(call: CallbackQuery):
    markup = await lifestyle_keyboard()
    await call.message.edit_text(f'Чем вы занимаетесь?', reply_markup=markup)
    await NewData.hobbies.set()


@dp.callback_query_handler(state=NewData.hobbies)
async def change_style(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    if call.data == 'study_lifestyle':
        try:
            await db.update_user_lifestyle(lifestyle='Учусь', telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь вы учитесь!')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка', reply_markup=markup)
            await state.reset_state()
    elif call.data == 'work_lifestyle':
        try:
            await db.update_user_lifestyle(lifestyle='Работаю', telegram_id=call.from_user.id)
            await call.message.edit_text('Теперь вы работаете!')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка', reply_markup=markup)
            await state.reset_state()
    elif call.data == 'job_find_lifestyle':
        try:
            await db.update_user_lifestyle(lifestyle='Ищу работу', telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь вы ищете работу!')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка', reply_markup=markup)
            await state.reset_state()
    elif call.data == 'householder_lifestyle':
        try:
            await db.update_user_lifestyle(lifestyle='Домохозяйка/Домохозяин', telegram_id=call.from_user.id)
            await call.message.edit_text(f'Теперь вы домохозяин/домохозяйка!')
            await asyncio.sleep(3)
            await call.message.edit_text(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f'Произошла неизвестная ошибка', reply_markup=markup)
            await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='photo')
async def new_photo(call: CallbackQuery):
    await call.message.edit_text(f'Отправьте мне новую фотографию')
    await NewData.photo.set()
    await asyncio.sleep(5)
    await delete_message(call.message)


@dp.message_handler(content_types=ContentType.PHOTO, state=NewData.photo)
async def update_photo_complete(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    file_id = message.photo[-1].file_id
    try:
        await db.update_user_photo_id(photo_id=file_id, telegram_id=message.from_user.id)
        await message.answer(f'Фото принято!')
        await asyncio.sleep(3)
        await delete_message(message)
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n'
                             f'Если ошибка осталась, напишите системному администратору.')
        await state.reset_state()


@dp.callback_query_handler(text='about_me')
async def new_comment(call: CallbackQuery):
    await call.message.edit_text(f'Отправьте мне новое описание анкеты: ')
    await NewData.commentary.set()


@dp.message_handler(state=NewData.commentary)
async def update_comment_complete(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        await db.update_user_commentary(commentary=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Комментарий принят!')
        await asyncio.sleep(3)
        await delete_message(message)
        await message.answer(f'Выберите, что вы хотите изменить: ', reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла ошибка! Попробуйте еще раз изменить описание. '
                             f'Возможно, Ваше сообщение слишком большое\n'
                             f'Если ошибка осталась, напишите системному администратору.')
        await state.reset_state()
