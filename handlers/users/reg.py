from keyboards.inline.lifestyle_choice_inline import lifestyle_inline_kb
from keyboards.inline.profile_bt import reg_profile
from aiogram.types import CallbackQuery, ContentType
from keyboards.inline.menu_inline import btn_pref
from aiogram.dispatcher import FSMContext
from states.reg_state import RegData
from loader import dp, bot, db
from aiogram import types
import asyncpg


@dp.callback_query_handler(text='registration')
# @dp.message_handler(Command("registration"))
async def registration(call: CallbackQuery):
    await bot.send_message(call.from_user.id, f"Пройдите опрос, чтобы зарегистрироваться", reply_markup=reg_profile)


@dp.callback_query_handler(text_contains="survey")
async def survey(call: CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Мужской', callback_data='male_reg')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Женский', callback_data='female_reg')
    keyboard.add(btn2)

    await bot.send_message(call.from_user.id, "Выберите пол", reply_markup=keyboard)
    await RegData.sex.set()


@dp.callback_query_handler(text='male_reg', state=RegData.sex)
@dp.callback_query_handler(text='female_reg', state=RegData.sex)
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

    await bot.send_message(call.from_user.id, f'Теперь напишите немного о себе: \n\n(255 символов max.)')
    await RegData.commentary.set()


@dp.message_handler(state=RegData.commentary)
async def commentary_reg(message: types.Message):
    try:
        await db.update_user_commentary(commentary=message.text, telegram_id=message.from_user.id)
        await message.reply(f'Комментарий принят!')
    except:
        await message.reply(f'Произошла неизвестная ошибка! Попробуйте изменить комментарий позже в разделе '
                            f'"Меню"')
    await bot.send_message(message.from_user.id, f'Выберите, кого вы хотите найти: ', reply_markup=btn_pref)
    await RegData.need_partner_sex.set()


@dp.callback_query_handler(text='male', state=RegData.need_partner_sex)
@dp.callback_query_handler(text='g_fe', state=RegData.need_partner_sex)
async def sex_reg(call: CallbackQuery):
    if call.data == 'male':
        try:
            await db.update_user_need_partner_sex(telegram_id=call.from_user.id, need_partner_sex='Мужской')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'g_fe':
        try:
            await db.update_user_need_partner_sex(telegram_id=call.from_user.id, need_partner_sex='Женский')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)

    await bot.send_message(call.from_user.id,
                           f'Отлично! Теперь напишите мне ваше имя, которое будут все видеть в анкете')
    await RegData.name.set()


@dp.message_handler(state=RegData.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    try:
        await db.update_user_varname(telegram_id=message.from_user.id, varname=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        print(err)

    # await delete_last_messages(bot, message)

    await bot.send_message(message.from_user.id, "Введите сколько вам лет:")

    await RegData.age.set()


@dp.message_handler(state=RegData.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)

    try:
        await db.update_user_age(telegram_id=message.from_user.id, age=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        print(err)

    # await delete_last_messages(bot, message)

    await bot.send_message(message.from_user.id, "Введите вашу национальность:")

    await RegData.nationality.set()


@dp.message_handler(state=RegData.nationality)
async def get_nationality(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Высшее', callback_data='higher_edu')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Среднее', callback_data='secondary_edu')
    keyboard.add(btn2)
    await state.update_data(nationality=message.text)

    try:
        await db.update_user_national(telegram_id=message.from_user.id, national=message.text)
        await state.update_data(nationality=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        print(err)

    # await delete_last_messages(bot, message)

    await bot.send_message(message.from_user.id, "Введите ваше образование:", reply_markup=keyboard)

    await RegData.education.set()


@dp.callback_query_handler(text='higher_edu', state=RegData.education)
@dp.callback_query_handler(text='secondary_edu', state=RegData.education)
async def get_education(call: CallbackQuery, state=FSMContext):
    # await state.update_data(education=message.text)

    if call.data == 'higher_edu':
        try:
            await db.update_user_education(telegram_id=call.from_user.id, education='Высшее')
            await state.update_data(education='Высшее')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)
    elif call.data == 'secondary_edu':
        try:
            await db.update_user_education(telegram_id=call.from_user.id, education='Среднее')
            await state.update_data(education='Среднее')
        except asyncpg.exceptions.UniqueViolationError as err:
            print(err)

    # await delete_last_call(bot, call)

    await bot.send_message(chat_id=call.from_user.id, text="Введите город в котором проживаете:")

    await RegData.town.set()


@dp.message_handler(state=RegData.town)
async def get_town(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='car_true')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='car_false')
    keyboard.add(btn2)
    # await state.update_data(town=message.text)
    try:
        await db.update_user_city(telegram_id=message.from_user.id, city=message.text)
        await state.update_data(town=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        print(err)
    # await delete_last_messages(bot, message)

    await bot.send_message(message.from_user.id, "Имеете ли вы машину:", reply_markup=keyboard)

    await RegData.car.set()


@dp.callback_query_handler(text=['car_true'], state=RegData.car)
@dp.callback_query_handler(text=['car_false'], state=RegData.car)
async def get_car(call: CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='apart_true')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='apart_false')
    keyboard.add(btn2)
    # await state.update_data(car=call.data)
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

    # await delete_last_call(bot, call)

    await bot.send_message(call.from_user.id, "Имеете ли вы свое жилье:", reply_markup=keyboard)

    await RegData.own_home.set()


@dp.callback_query_handler(text_contains=['apart_true'], state=RegData.own_home)
@dp.callback_query_handler(text_contains=['apart_false'], state=RegData.own_home)
async def get_own_home(call: CallbackQuery, state: FSMContext):
    # await state.update_data(own_home=message.text)

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

    # await delete_last_call(bot, call)

    await bot.send_message(call.from_user.id, "Чем вы занимаетесь:", reply_markup=lifestyle_inline_kb)

    await RegData.hobbies.set()


@dp.callback_query_handler(state=RegData.hobbies,
                           text_contains=['study_lifestyle'])
@dp.callback_query_handler(state=RegData.hobbies,
                           text_contains=['work_lifestyle'])
@dp.callback_query_handler(state=RegData.hobbies,
                           text_contains=['job_find_lifestyle'])
@dp.callback_query_handler(state=RegData.hobbies,
                           text_contains=['householder_lifestyle'])
async def get_hobbies(call: CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Занят', callback_data='busy')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Не занят', callback_data='not_busy')
    keyboard.add(btn2)

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

    # await delete_last_call(bot, call)

    await bot.send_message(call.from_user.id, "Выберите ваше семейное положение", reply_markup=keyboard)

    await RegData.marital.set()


@dp.callback_query_handler(text_contains='busy', state=RegData.marital)
@dp.callback_query_handler(text_contains='not_busy', state=RegData.marital)
async def get_marital(call: CallbackQuery, state=FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='true')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='false')
    keyboard.add(btn2)

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

    await bot.send_message(call.from_user.id, "Есть ли у вас дети?", reply_markup=keyboard)
    await RegData.child.set()


@dp.callback_query_handler(text_contains=['true'], state=RegData.child)
@dp.callback_query_handler(text_contains=['false'], state=RegData.child)
async def get_childs(call: CallbackQuery, state=FSMContext):
    # await state.update_data(child=message.text)

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

    await bot.send_message(call.from_user.id, f'И напоследок, отправьте мне Вашу фотографию')
    await RegData.photo.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=RegData.photo)
async def get_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[0].file_id
    try:
        await db.update_user_photo_id(photo_id=file_id, telegram_id=message.from_user.id)
        await message.reply(f'Фото принято!')
    except:
        await message.reply(f'Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n'
                            f'Если ошибка осталась, напишите системному администратору.')
    # await delete_last_call(bot, call)

    user_data = await state.get_data()

    await state.finish()

    user = await db.select_user(telegram_id=message.from_user.id)
    print(user)

    username = user.get('varname')
    userage = user.get('age')
    usersex = user.get('sex')
    usernational = user.get('national')
    usereducation = user.get('education')
    usercity = user.get('city')

    usercar = user.get('car')
    if usercar == True:
        usercar = 'Есть машина'
    elif usercar == False:
        usercar = 'Нет машины'

    userapart = user.get('apartment')
    if userapart == True:
        userapart = 'Есть квартира'
    elif userapart == False:
        userapart = 'Нет квартиры'

    userlifestyle = user.get('lifestyle')

    userkids = user.get('kids')
    if userkids == True:
        userkids = 'Есть дети'
    elif userkids == False:
        userkids = 'Нет детей'

    usermarital = user.get('marital')
    usercomm = user.get('commentary')

    await bot.send_message(message.from_user.id, "Вы успешно зарегистрированы")
    await bot.send_photo(
        message.from_user.id, caption=f"1. Ваше имя - {str(username)}\n"
                                      f"2. Ваш возраст - {str(userage)}\n"
                                      f"3. Ваш пол - {str(usersex)}\n"
                                      f"4. Ваша национальность - {str(usernational)}\n"
                                      f"5. Ваше образование - {str(usereducation)}\n"
                                      f"6. Ваш город - {str(usercity)}\n"
                                      f"7. Наличие машины - {str(usercar)}\n"
                                      f"8. Наличие жилья - {str(userapart)}\n"
                                      f"9. Ваше занятие - {str(userlifestyle)}\n"
                                      f"10. Наличие детей - {str(userkids)}\n"
                                      f"11. Семейное положение - {str(usermarital)}\n\n"
                                      f"12. О себе - {str(usercomm)}",
        photo=user.get('photo_id')
    )
