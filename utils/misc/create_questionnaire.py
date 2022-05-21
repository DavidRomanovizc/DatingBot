from keyboards.inline.questionnaires_inline import reciprocity_keyboard, questionnaires_keyboard, back_viewing_ques_keyboard
from utils.db_api import db_commands
from loader import bot


async def get_data(telegram_id: int):
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_name = user.get("varname")
    user_age = user.get("age")
    user_sex = user.get("sex")
    user_city = user.get("city")
    user_life_style = user.get("lifestyle")
    user_comm = user.get("commentary")
    user_verification = user.get("verification")
    photo_random_user = user.get("photo_id")
    user_inst = user.get("instagram")
    user_status = user.get("status")
    user_need_gender = user.get("need_partner_sex")

    if user_inst is None:
        user_inst = "Пользователь не прикрепил Instagram"
    if photo_random_user is None:
        photo_random_user = "https://www.meme-arsenal.com/memes/5eae5104f379baa355e031fa1ded886c.jpg"
    if user_verification:
        user_verification = '✅ Подтвержденный'
    else:
        user_verification = '❌ Неподтвержденный'
    if user_name is None:
        user_name = "Не определено"
    if user_sex is None:
        user_sex = "Не определен"
    if user_city is None:
        user_city = "Не определен"
    if user_life_style is None:
        user_life_style = "Не определен"
    if user_comm is None:
        user_comm = "Пусто"

    return (
        user_name, user_age, user_sex, user_city,
        user_life_style, user_comm, user_verification, photo_random_user, user_inst, user_status, user_need_gender
    )


async def user_location(telegram_id: int):
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_longitude = user.get("longitude")
    user_latitude = user.get("latitude")
    return user_longitude, user_latitude


async def get_data_filters(telegram_id: int):
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_need_age_min = user.get("need_partner_age_min")
    user_need_age_max = user.get("need_partner_age_max")
    user_need_range = user.get("need_partner_range")
    return user_need_age_min, user_need_age_max, user_need_range


async def find_user_gender(telegram_id):
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_sex = user.get("need_partner_sex")
    user_need_gender = await db_commands.search_user(user_sex)
    lst = []
    for i in range(len(user_need_gender)):
        lst.append(user_need_gender[i]['telegram_id'])

    return lst


async def send_questionnaire(chat_id, user_data, markup=None, add_text=None):
    if add_text is None:
        await bot.send_photo(chat_id=chat_id, caption=f"<b>Статус анкеты</b> - \n{str(user_data[6])}\n\n"
                                                      f"<b>Имя</b> - {str(user_data[0])}\n"
                                                      f"<b>Возраст</b> - {str(user_data[1])}\n"
                                                      f"<b>Пол</b> - {str(user_data[2])}\n"
                                                      f"<b>Город</b> - {str(user_data[3])}\n"
                                                      f"<b>Ваше занятие</b> - {str(user_data[4])}\n"
                                                      f"<b>О себе</b> - {str(user_data[5])}\n\n",
                             photo=user_data[7], reply_markup=await questionnaires_keyboard())
    elif markup is None:
        await bot.send_photo(chat_id=chat_id, caption=f"{add_text}\n\n"
                                                      f"<b>Статус анкеты</b> - \n{str(user_data[6])}\n\n"
                                                      f"<b>Имя</b> - {str(user_data[0])}\n"
                                                      f"<b>Возраст</b> - {str(user_data[1])}\n"
                                                      f"<b>Пол</b> - {str(user_data[2])}\n"
                                                      f"<b>Город</b> - {str(user_data[3])}\n"
                                                      f"<b>Ваше занятие</b> - {str(user_data[4])}\n"
                                                      f"<b>О себе</b> - {str(user_data[5])}\n\n",
                             photo=user_data[7], reply_markup=await back_viewing_ques_keyboard())

    else:
        await bot.send_photo(chat_id=chat_id, caption=f"{add_text}\n\n"
                                                      f"<b>Статус анкеты</b> - \n{str(user_data[6])}\n\n"
                                                      f"<b>Имя</b> - {str(user_data[0])}\n"
                                                      f"<b>Возраст</b> - {str(user_data[1])}\n"
                                                      f"<b>Пол</b> - {str(user_data[2])}\n"
                                                      f"<b>Город</b> - {str(user_data[3])}\n"
                                                      f"<b>Ваше занятие</b> - {str(user_data[4])}\n"
                                                      f"<b>О себе</b> - {str(user_data[5])}\n\n",
                             photo=user_data[7], reply_markup=await reciprocity_keyboard())


async def create_questionnaire(state, random_user, chat_id, add_text=None):
    markup = await questionnaires_keyboard()
    user_data = await get_data(random_user)
    await send_questionnaire(chat_id=chat_id, user_data=user_data, markup=markup, add_text=add_text)
    await state.update_data(data={'questionnaire_owner': random_user})


async def create_questionnaire_reciprocity(state, random_user, chat_id, add_text=None):
    user_data = await get_data(random_user)
    await send_questionnaire(chat_id=chat_id, user_data=user_data, add_text=add_text)
    await state.update_data(data={'questionnaire_owner': random_user})


async def get_meeting_data(telegram_id):
    user = await db_commands.select_meetings_user(telegram_id=telegram_id)

    user_name = user.get("username")
    meeting_description = user.get("meetings_description")

    return (
        user_name, meeting_description
    )


async def select_all_users_list(telegram_id: int):
    users_records = await db_commands.select_all_user_meetings()
    list_id = []
    for i in users_records:
        id_user = i.get('telegram_id')
        list_id.append(id_user)
    list_id.remove(telegram_id)
    for j in list_id:
        user = await get_meeting_data(j)
        if user[1] is None:
            list_id.remove(j)
    return list_id


async def send_ques_meeting(chat_id, user_data, markup):
    await bot.send_message(chat_id=chat_id, text=f"{user_data[1]}\n\n"
                                                 f'<a href="https://t.me/{user_data[0]}">{user_data[0]}</a>',
                           reply_markup=markup)
