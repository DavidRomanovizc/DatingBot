from utils.db_api import db_commands


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
        user_verification = 'Подтвержденный'
    else:
        user_verification = 'Неподтвержденный'
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