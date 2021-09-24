from keyboards.inline.lifestyle_choice_inline import lifestyle_inline_kb
from keyboards.inline.change_profile_inline import change_profile_kb
from aiogram.types import CallbackQuery, ContentType
from states.new_data_state import NewData
from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from aiogram import types


@dp.callback_query_handler(text='change_profile')
async def start_change_data(call: CallbackQuery):
    await bot.send_message(call.from_user.id, f'Выберите, что вы хотите изменить: ', reply_markup=change_profile_kb)


@dp.message_handler(text='Имя')
async def change_name(message: types.Message):
    await message.reply(f'Введите новое имя')
    await NewData.name.set()


@dp.message_handler(state=NewData.name)
async def change_name(message: types.Message, state: FSMContext):
    try:
        await db.update_user_varname(varname=message.text, telegram_id=message.from_user.id)
        await message.reply(f'Ваше новое имя: <b>{message.text}</b>')
        await state.reset_state()
    except:
        await message.reply(f'Произошла незвестная ошибка')
        await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Возраст')
async def change_name(message: types.Message):
    await message.reply(f'Введите новый возраст')
    await NewData.age.set()


@dp.message_handler(state=NewData.age)
async def change_name(message: types.Message, state: FSMContext):
    try:
        await db.update_user_age(age=message.text, telegram_id=message.from_user.id)
        await message.reply(f'Ваш новый возраст: <b>{message.text}</b>')
        await state.reset_state()

    except:
        await message.reply(f'Произошла незвестная ошибка')
        await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Национальность')
async def change_name(message: types.Message):
    await message.reply(f'Введите новую национальность')
    await NewData.nationality.set()


@dp.message_handler(state=NewData.nationality)
async def change_name(message: types.Message, state: FSMContext):
    try:
        await db.update_user_national(national=message.text, telegram_id=message.from_user.id)
        await message.reply(f'Ваша новая национальность: <b>{message.text}</b>')
        await state.reset_state()
    except:
        await message.reply(f'Произошла незвестная ошибка')
        await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Город')
async def change_cuty(message: types.Message):
    await message.reply(f'Введите новый город')
    await NewData.city.set()


@dp.message_handler(state=NewData.city)
async def change_city(message: types.Message, state: FSMContext):
    try:
        await db.update_user_city(city=message.text, telegram_id=message.from_user.id)
        await message.reply(f'Ваш новый город: <b>{message.text}</b>')
        await state.reset_state()
    except:
        await message.reply(f'Произошла незвестная ошибка')
        await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Пол')
async def change_sex(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Мужской', callback_data='male')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Женский', callback_data='female')
    keyboard.add(btn2)
    await message.reply(f'Выберите новый пол: ', reply_markup=keyboard)
    await NewData.sex.set()


@dp.callback_query_handler(text='male', state=NewData.sex)
@dp.callback_query_handler(text='female', state=NewData.sex)
async def change_sex(call: CallbackQuery, state: FSMContext):
    if call.data == 'male':
        try:
            await db.update_user_sex(sex='Мужской', telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Ваш новый пол: <b>Мужской</b>')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()
    if call.data == 'female':
        try:
            await db.update_user_sex(sex='Женский', telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Ваш новый пол: <b>Женский</b>')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Машина')
async def change_car(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Есть', callback_data='true')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='false')
    keyboard.add(btn2)
    await message.reply(f'Есть ли у Вас машина?: ', reply_markup=keyboard)
    await NewData.car.set()


@dp.callback_query_handler(text='true', state=NewData.car)
@dp.callback_query_handler(text='false', state=NewData.car)
async def change_car(call: CallbackQuery, state: FSMContext):
    if call.data == 'true':
        try:
            await db.update_user_car(car=True, telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь у вас: <b>есть</b> машина')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()
    if call.data == 'false':
        try:
            await db.update_user_car(car=False, telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь у вас: <b>нет</b> машины')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Дети')
async def change_kids(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Есть', callback_data='true')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='false')
    keyboard.add(btn2)
    await message.reply(f'Есть ли у Вас дети?: ', reply_markup=keyboard)
    await NewData.child.set()


@dp.callback_query_handler(text='true', state=NewData.child)
@dp.callback_query_handler(text='false', state=NewData.child)
async def change_name(call: CallbackQuery, state: FSMContext):
    if call.data == 'true':
        try:
            await db.update_user_kids(kids=True, telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь у вас: <b>есть</b> дети')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()
    if call.data == 'false':
        try:
            await db.update_user_kids(kids=False, telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь у вас: <b>нет</b> детей')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Жилье')
async def change_kids(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Есть', callback_data='true')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='false')
    keyboard.add(btn2)
    await message.reply(f'Есть ли у Вас квартира: ', reply_markup=keyboard)
    await NewData.own_home.set()


@dp.callback_query_handler(text='true', state=NewData.own_home)
@dp.callback_query_handler(text='false', state=NewData.own_home)
async def change_name(call: CallbackQuery, state: FSMContext):
    if call.data == 'true':
        try:
            await db.update_user_apartment(apartment=True, telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь у вас: <b>есть</b> квартира')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()
    if call.data == 'false':
        try:
            await db.update_user_apartment(apartment=False, telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь у вас: <b>нет</b> квартиры')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Образование')
async def change_kids(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Высшее', callback_data='higher_edu')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Среднее', callback_data='secondary_edu')
    keyboard.add(btn2)
    await message.reply(f'Какое у Вас образование: ', reply_markup=keyboard)
    await NewData.education.set()


@dp.callback_query_handler(text='higher_edu', state=NewData.education)
@dp.callback_query_handler(text='secondary_edu', state=NewData.education)
async def change_name(call: CallbackQuery, state: FSMContext):
    if call.data == 'higher_edu':
        try:
            await db.update_user_apartment(apartment=True, telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь у вас: <b>Высшее</b> образование')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()
    if call.data == 'secondary_edu':
        try:
            await db.update_user_apartment(apartment=False, telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь у вас: <b>Среднее</b> образование')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Занятие')
async def change_kids(message: types.Message):
    await message.reply(f'Чем вы занимаетесь?', reply_markup=lifestyle_inline_kb)
    await NewData.hobbies.set()


@dp.callback_query_handler(state=NewData.hobbies,
                           text_contains=['study_lifestyle'])
@dp.callback_query_handler(state=NewData.hobbies,
                           text_contains=['work_lifestyle'])
@dp.callback_query_handler(state=NewData.hobbies,
                           text_contains=['job_find_lifestyle'])
@dp.callback_query_handler(state=NewData.hobbies,
                           text_contains=['householder_lifestyle'])
async def change_name(call: CallbackQuery, state: FSMContext):
    if call.data == 'study_lifestyle':
        try:
            await db.update_user_lifestyle(lifestyle='Учусь', telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь вы учитесь!')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()
    elif call.data == 'work_lifestyle':
        try:
            await db.update_user_lifestyle(lifestyle='Работаю', telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь вы работаете!')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()
    elif call.data == 'job_find_lifestyle':
        try:
            await db.update_user_lifestyle(lifestyle='Ищу работу', telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь вы ищете работу!')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()
    elif call.data == 'householder_lifestyle':
        try:
            await db.update_user_lifestyle(lifestyle='Домохозяйка/Домохозяин', telegram_id=call.from_user.id)
            await bot.send_message(call.from_user.id, f'Теперь вы домохозяин/домохозяйка!')
            await state.reset_state()
        except:
            await bot.send_message(call.from_user.id, f'Произошла незвестная ошибка')
            await state.reset_state()

    await state.reset_state()


@dp.message_handler(text='Фото')
async def new_photo(message: types.Message):
    await message.reply(f'Отправьте мне новую фотографию')
    await NewData.photo.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=NewData.photo)
async def update_photo_complete(message: types.Message, state: FSMContext):
    file_id = message.photo[0].file_id
    try:
        await db.update_user_photo_id(photo_id=file_id, telegram_id=message.from_user.id)
        await message.reply(f'Фото принято!')
        await state.reset_state()
    except:
        await message.reply(f'Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n'
                            f'Если ошибка осталась, напишите системному администратору.')
        await state.reset_state()


@dp.message_handler(text='О себе')
async def new_photo(message: types.Message):
    await message.reply(f'Отправьте мне новое описание анкеты: ')
    await NewData.commentary.set()


@dp.message_handler(state=NewData.commentary)
async def update_photo_complete(message: types.Message, state: FSMContext):
    try:
        await db.update_user_commentary(commentary=message.text, telegram_id=message.from_user.id)
        await message.reply(f'Комментарий принят!')
        await state.reset_state()
    except:
        await message.reply(f'Произошла ошибка! Попробуйте еще раз изменить описание. '
                            f'Возможно, Ваше сообщение слишком большое\n'
                            f'Если ошибка осталась, напишите системному администратору.')
        await state.reset_state()
