from utils.db_api import db_commands


async def get_data(telegram_id):
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_name = user.get('varname')
    user_age = user.get('age')
    user_sex = user.get('sex')
    user_national = user.get('national')
    user_education = user.get('education')
    user_city = user.get('city')
    user_apart = user.get('apartment')
    user_car = user.get('car')
    user_life_style = user.get('lifestyle')
    user_kids = user.get('kids')
    user_marital = user.get('marital')
    user_comm = user.get('commentary')
    user_verification = user.get('verification')

    if user_verification:
        user_verification = '✅ Подтвержденный'
    else:
        user_verification = '❌ Неподтвержденный'

    if user_car:
        user_car = 'Есть машина'
    else:
        user_car = 'Нет машины'

    if user_apart:
        user_apart = 'Есть квартира'
    else:
        user_apart = 'Нет квартиры'

    if user_kids:
        user_kids = 'Есть дети'
    else:
        user_kids = 'Нет детей'

    return (
        user_name, user_age, user_sex, user_national, user_education, user_city, user_car, user_apart,
        user_life_style, user_kids, user_marital, user_comm, user_verification
    )
