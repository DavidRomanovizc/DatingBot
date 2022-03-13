from keyboards.inline.second_menu import menu_inline_kb, btn_pref
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp, db, bot
import logging


@dp.callback_query_handler(text="second_m")
async def open_menu(call: CallbackQuery):
    await call.message.edit_text(f"Меню: ",
                                 reply_markup=menu_inline_kb)


@dp.callback_query_handler(text="my_profile")
async def my_profile_menu(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Назад", callback_data="back_with_delete")
    keyboard.add(btn1)
    user = await db.select_user(telegram_id=call.from_user.id)

    user_name = user.get('varname')
    user_age = user.get('age')
    user_sex = user.get('sex')
    user_national = user.get('national')
    user_education = user.get('education')
    user_city = user.get('city')

    usercar = user.get('car')
    if usercar:
        usercar = 'Есть машина'
    else:
        usercar = 'Нет машины'

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
                                            f'{usercar}\n'
                                            f'{user_apart}\n'
                                            f'{user_kids}\n\n'
                                            f'{user_lifestyle}\n\n'
                                            f'Обо мне: {str(user_comm)}',
                                    photo=user_photo, reply_markup=keyboard)


@dp.callback_query_handler(text_contains="preferences")
async def get_preferences(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data

    logging.info(f"{callback_data}=")
    await call.message.edit_text("Кого вы ищете? ", reply_markup=btn_pref)


@dp.callback_query_handler(text_contains="male")
async def get_male(call: CallbackQuery):
    callback_data = call.data

    logging.info(f"{callback_data}=")
    await db.update_user_need_partner_sex(need_partner_sex='Мужской', telegram_id=call.from_user.id)
    await call.message.edit_text("Вы выбрали мужчин", reply_markup=menu_inline_kb)


@dp.callback_query_handler(text_contains="g_fe")
async def get_male(call: CallbackQuery):
    callback_data = call.data

    logging.info(f"{callback_data}=")
    await db.update_user_need_partner_sex(need_partner_sex='Женский', telegram_id=call.from_user.id)
    await call.message.edit_text("Вы выбрали женщин", reply_markup=menu_inline_kb)
