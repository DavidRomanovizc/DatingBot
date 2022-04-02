from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.second_menu_inline import second_menu_keyboard
from handlers.users.back_handler import delete_message

from utils.db_api import db_commands
from loader import dp


@dp.callback_query_handler(text="second_m")
async def open_menu(call: CallbackQuery):
    markup = await second_menu_keyboard()
    await call.message.edit_text(f"<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                                 f"<b>🤝 Сотрудничество: </b>\n"
                                 f"Если у вас есть предложение о сотрудничестве, пишите сюда - "
                                 f"@DRomanovizc\n\n",
                                 reply_markup=markup)


@dp.callback_query_handler(text="my_profile")
async def my_profile_menu(call: CallbackQuery):
    await delete_message(call.message)
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Назад", callback_data="back_to_sec_menu")
    keyboard.add(btn1)

    user = await db_commands.select_user(telegram_id=call.from_user.id)
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

    user_lifestyle = user.get('lifestyle')

    user_kids = user.get('kids')
    if user_kids:
        user_kids = 'Есть дети'
    else:
        user_kids = 'Нет детей'
    user_comm = user.get('commentary')
    user_photo = user.get('photo_id')
    if user_photo:
        user_photo = user.get('photo_id')
    elif user_photo is None:
        user_photo = 'https://www.pngfind.com/pngs/m/110-1102775_download-empty-profile-hd-png-download.png'

    await call.message.answer_photo(caption=f'{str(user_name)}, {str(user_age)}\n\n'
                                            f'{user_sex}, {str(user_city)}, {str(user_national)}\n\n'
                                            f'{user_education}\n'
                                            f'{user_car}\n'
                                            f'{user_apart}\n'
                                            f'{user_kids}\n\n'
                                            f'{user_lifestyle}\n\n'
                                            f'Обо мне: {str(user_comm)}',
                                    photo=user_photo, reply_markup=keyboard)

