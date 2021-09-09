####################################

##################FREEZED###########
##       ACTIVE_FILE_IN              handlers/users/change_datas.py
####################################

user_data = {
    "name": "1",
    "age": "2",
    "nationality": "3",
    "education": "4",
    "town": "5",
    "car": "6",
    "own_home": "7",
    "hobbies": "8",
    "child": "9",
    "marital": "10"
}

responce_for_user = {
    "name": "Введите ваше имя",
    "age": "Введите сколько вам лет",
    "nationality": "Введите вашу национальность",
    "education": "Введите ваше образование",
    "town": "Введите город в котором проживаете",
    "car": "Емеете ли вы машину",
    "own_home": "Есть ли у вас собственное место жительства",
    "hobbies": "Чем вы занимаетесь",
    "child": "Есть ли у вас дети",
    "marital": "Выберите семейное положение"
}


# эта функия дубликат функции in reg.py, нужно будет в одно место закинуть
async def delete_last_messages(bot, message):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)


@dp.callback_query_handler()  # обработчик для клавиш редактирования
async def query_handler(calldata: types.CallbackQuery, state: FSMContext):
    await state.update_data(new_data=calldata.data)

    await NewData.new_data_state.set()
    await bot.send_message(
        calldata.from_user.id,
        responce_for_user.get(calldata.data)
    )


@dp.message_handler(state=NewData.new_data_state)
async def recv_and_save_new_info(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data.get("new_data"), " --- ", message.text)

    # следующий код(сторка 49) нужно повторить для каждого пункта из анкеты
    # было бы лучше так --> "UPDATE users SET {user_data.get("new_data")} = {message.text} WHERE telegram_id = {message.from_user.id}"
    # типо получить что сейчас вводит юзер и записать в ту колонку которая соответствует,
    # ид мы знаем и текст мы тоже знаем, но это нужно сменить названия колонок в таблицах.
    # Но таким способом просто не нужно делать проверки
    # Кто читает тот PHP-шник

    if user_data.get("new_data") == "name":
        await db.update_user_varname(varname=message.text, telegram_id=message.from_user.id)
    elif user_data.get("new_data") == "age":
        await db.update_user_age(age=message.text, telegram_id=message.from_user.id)
    elif user_data.get("new_data") == "nationality":
        await db.update_user_national(national=message.text, telegram_id=message.from_user.id)
    elif user_data.get("new_data") == "education":
        await db.update_user_education(education=message.text, telegram_id=message.from_user.id)
    elif user_data.get("new_data") == "town":
        await db.update_user_town(town=message.text, telegram_id=message.from_user.id)
    # elif user_data.get("new_data") == "car":
    #     await db.update_user_car(car=message.text, telegram_id=message.from_user.id)
    # elif user_data.get("new_data") == "own_home":
    #     await db.update_user_apartment(apartment=message.text, telegram_id=message.from_user.id)
    elif user_data.get("new_data") == "hobbies":
        await db.update_user_lifestyle(lifestyle=message.text, telegram_id=message.from_user.id)
    # elif user_data.get("new_data") == "child":
    #     await db.update_user_kids(kids=message.text, telegram_id=message.from_user.id)
    elif user_data.get("new_data") == "marital":
        await db.update_user_marital(marital=message.text, telegram_id=message.from_user.id)

    await state.finish()


@dp.message_handler(commands=["changedata"])
async def chande_data(message: types.Message):
    # TODO: тут нужно запросить данные из бд. но пока использую словарь

    for key, value in MarupDatas.ALL_INFO.items():  # создание клавиш
        change_Keyboard.add(
            InlineKeyboardButton(
                text=key + user_data[value], callback_data=value  # тут нужо будет данные с бд вставить
            )
        )

    await bot.send_message(
        message.chat.id,
        "Выбирете что хотите изменить:",
        reply_markup=change_Keyboard
    )
