import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from loguru import logger

from keyboards.inline.lifestyle_choice_inline import lifestyle_keyboard
from keyboards.inline.profile_bt import registration_keyboard
from keyboards.inline.second_menu import menu_inline_kb
from keyboards.inline.sex_partner import sex_partner

from loader import dp, db
from states.reg_state import RegData


@dp.callback_query_handler(text='registration')
async def registration(call: CallbackQuery):
    markup = await registration_keyboard()
    text = f"Пройдите опрос, чтобы зарегистрироваться"
    await call.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(text_contains="survey")
async def survey(call: CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_with=1)
    btn1 = types.InlineKeyboardButton(text='Мужской', callback_data='male_reg')
    btn2 = types.InlineKeyboardButton(text='Женский', callback_data='female_reg')
    keyboard.add(btn1, btn2)

    await call.message.edit_text("Выберите пол", reply_markup=keyboard)
    await RegData.sex.set()


@dp.callback_query_handler(state=RegData.sex)
async def sex_reg(call: CallbackQuery):
    if call.data == 'male_reg':
        try:
            await db.update_user_sex(telegram_id=call.from_user.id, sex='Мужской')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'female_reg':
        try:
            await db.update_user_sex(telegram_id=call.from_user.id, sex='Женский')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)

    await call.message.edit_text(f'Теперь напишите немного о себе: \n\n(255 символов max.)')
    await RegData.commentary.set()


@dp.message_handler(state=RegData.commentary)
async def commentary_reg(message: types.Message):
    markup = await sex_partner()
    try:
        await db.update_user_commentary(commentary=message.text, telegram_id=message.from_user.id)
        await message.reply(f'Комментарий принят! Выберите, кого вы хотите найти: ', reply_markup=markup)
    except Exception as err:
        logger.error(err)
        await message.reply(f'Произошла неизвестная ошибка! Попробуйте изменить комментарий позже в разделе '
                            f'"Меню"\n\n'
                            f'Выберите, кого вы хотите найти: ', reply_markup=markup)
    await RegData.need_partner_sex.set()


@dp.callback_query_handler(state=RegData.need_partner_sex)
async def sex_reg(call: CallbackQuery):
    if call.data == 'gen_male':
        try:
            await db.update_user_need_partner_sex(telegram_id=call.from_user.id, need_partner_sex='Мужской')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'g_fe':
        try:
            await db.update_user_need_partner_sex(telegram_id=call.from_user.id, need_partner_sex='Женский')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)

    await call.message.edit_text(f'Отлично! Теперь напишите мне ваше имя, которое будут все видеть в анкете')
    await RegData.name.set()


@dp.message_handler(state=RegData.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    try:
        await db.update_user_varname(telegram_id=message.from_user.id, varname=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        print(err)
    await message.reply("Введите сколько вам лет:")
    await RegData.age.set()


@dp.message_handler(state=RegData.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    try:
        await db.update_user_age(telegram_id=message.from_user.id, age=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        print(err)
    await message.reply("Введите вашу национальность:")
    await RegData.nationality.set()


@dp.message_handler(state=RegData.nationality)
async def get_nationality(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Высшее', callback_data='higher_edu')
    btn2 = types.InlineKeyboardButton(text='Среднее', callback_data='secondary_edu')
    keyboard.add(btn1, btn2)
    await state.update_data(nationality=message.text)

    try:
        await db.update_user_national(telegram_id=message.from_user.id, national=message.text)
        await state.update_data(nationality=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        print(err)
    await message.reply("Введите ваше образование:", reply_markup=keyboard)
    await RegData.education.set()


@dp.callback_query_handler(state=RegData.education)
async def get_education(call: CallbackQuery, state=FSMContext):
    if call.data == 'higher_edu':
        try:
            await db.update_user_education(telegram_id=call.from_user.id, education='Высшее')
            await state.update_data(education='Высшее')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'secondary_edu':
        try:
            await db.update_user_education(telegram_id=call.from_user.id, education='Среднее')
            await state.update_data(education="Среднее")
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    await call.message.edit_text(text="Введите город в котором проживаете:")
    await RegData.town.set()


@dp.message_handler(state=RegData.town)
async def get_town(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='car_true')
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='car_false')
    keyboard.add(btn1, btn2)
    try:
        await db.update_user_city(telegram_id=message.from_user.id, city=message.text)
        await state.update_data(town=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        print(err)
    await message.reply("Имеете ли вы машину:", reply_markup=keyboard)
    await RegData.car.set()


@dp.callback_query_handler(state=RegData.car)
async def get_car(call: CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='apart_true')
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='apart_false')
    keyboard.add(btn1, btn2)
    if call.data == 'car_true':
        try:
            await db.update_user_car(telegram_id=call.from_user.id, car=True)
            await state.update_data(car='Есть машина')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'car_false':
        try:
            await db.update_user_car(telegram_id=call.from_user.id, car=False)
            await state.update_data(car='Нет машины')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    await call.message.edit_text("Имеете ли вы свое жилье:", reply_markup=keyboard)
    await RegData.own_home.set()


@dp.callback_query_handler(state=RegData.own_home)
async def get_own_home(call: CallbackQuery, state: FSMContext):
    markup = await lifestyle_keyboard()
    if call.data == 'apart_true':
        try:
            await db.update_user_apartment(telegram_id=call.from_user.id, apartment=True)
            await state.update_data(own_home='Есть квартира')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'apart_false':
        try:
            await db.update_user_apartment(telegram_id=call.from_user.id, apartment=False)
            await state.update_data(own_home='Нет квартиры')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    await call.message.edit_text("Чем вы занимаетесь:", reply_markup=markup)
    await RegData.hobbies.set()


@dp.callback_query_handler(state=RegData.hobbies)
async def get_hobbies(call: CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Занят', callback_data='busy')
    btn2 = types.InlineKeyboardButton(text='Не занят', callback_data='not_busy')
    keyboard.add(btn1, btn2)

    if call.data == 'study_lifestyle':
        try:
            await db.update_user_lifestyle(telegram_id=call.from_user.id, lifestyle='Учусь')
            await state.update_data(hobbies='Учусь')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'work_lifestyle':
        try:
            await db.update_user_lifestyle(telegram_id=call.from_user.id, lifestyle='Работаю')
            await state.update_data(hobbies='Работаю')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'job_find_lifestyle':
        try:
            await db.update_user_lifestyle(telegram_id=call.from_user.id, lifestyle='Ищу работу')
            await state.update_data(hobbies='Ищу работу')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'householder_lifestyle':
        try:
            await db.update_user_lifestyle(telegram_id=call.from_user.id, lifestyle='Домохозяйка/Домохозяин')
            await state.update_data(hobbies='Домохозяйка/Домохозяин')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    await call.message.edit_text("Выберите ваше семейное положение", reply_markup=keyboard)
    await RegData.marital.set()


@dp.callback_query_handler(state=RegData.marital)
async def get_marital(call: CallbackQuery, state=FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='true')
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='false')
    keyboard.add(btn1, btn2)

    if call.data == 'busy':
        try:
            await db.update_user_marital(telegram_id=call.from_user.id, marital='Занят/a')
            await state.update_data(marital='Занят')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'not_busy':
        try:
            await db.update_user_marital(telegram_id=call.from_user.id, marital='Не занят/a')
            await state.update_data(marital='Не занят')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)

    await call.message.edit_text("Есть ли у вас дети?", reply_markup=keyboard)
    await RegData.child.set()


@dp.callback_query_handler(state=RegData.child)
async def get_children(call: CallbackQuery, state=FSMContext):
    if call.data == 'true':
        try:
            await db.update_user_kids(telegram_id=call.from_user.id, kids=True)
            await state.update_data(child='Есть дети')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'false':
        try:
            await db.update_user_kids(telegram_id=call.from_user.id, kids=False)
            await state.update_data(child='Нет детей')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    await call.message.edit_text(f'И напоследок, отправьте мне Вашу фотографию')
    await RegData.photo.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=RegData.photo)
async def get_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    try:
        await db.update_user_photo_id(photo_id=file_id, telegram_id=message.from_user.id)
        await message.reply(f'Фото принято!')
    except Exception as err:
        logger.error(err)
        await message.reply(f'Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n'
                            f'Если ошибка осталась, напишите системному администратору.')

    await state.finish()

    user = await db.select_user(telegram_id=message.from_user.id)
    print(user)

    user_name = user.get('varname')
    user_age = user.get('age')
    user_sex = user.get('sex')
    user_national = user.get('national')
    user_education = user.get('education')
    user_city = user.get('city')

    user_car = user.get('car')
    if user_car:
        user_car = 'Есть машина'
    else:
        user_car = 'Нет машины'

    user_apart = user.get('apartment')
    if user_apart:
        user_apart = 'Есть квартира'
    else:
        user_apart = 'Нет квартиры'

    user_life_style = user.get('lifestyle')

    user_kids = user.get('kids')
    if user_kids:
        user_kids = 'Есть дети'
    else:
        user_kids = 'Нет детей'

    user_marital = user.get('marital')
    user_comm = user.get('commentary')

    await message.answer_photo(caption=f"Регистрация завершена успешно! \n\n "
                                       f"1. Ваше имя - {str(user_name)}\n"
                                       f"2. Ваш возраст - {str(user_age)}\n"
                                       f"3. Ваш пол - {str(user_sex)}\n"
                                       f"4. Ваша национальность - {str(user_national)}\n"
                                       f"5. Ваше образование - {str(user_education)}\n"
                                       f"6. Ваш город - {str(user_city)}\n"
                                       f"7. Наличие машины - {str(user_car)}\n"
                                       f"8. Наличие жилья - {str(user_apart)}\n"
                                       f"9. Ваше занятие - {str(user_life_style)}\n"
                                       f"10. Наличие детей - {str(user_kids)}\n"
                                       f"11. Семейное положение - {str(user_marital)}\n\n"
                                       f"12. О себе - {str(user_comm)}\n\n",
                               photo=user.get('photo_id'))
    await message.answer("Меню: ", reply_markup=menu_inline_kb)
