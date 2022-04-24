from keyboards.inline.questionnaires_inline import reciprocity_keyboard, questionnaires_keyboard
from loader import bot
from utils.db_api import db_commands
from utils.db_api.db_commands import search_user


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
    user_need_gender = await search_user(user_sex)
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
                             photo=user_data[7])

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
