from keyboards.inline.inline_start_menu import inline_start
from keyboards.inline.menu_inline import menu_inline_kb, btn_pref
from aiogram.types import CallbackQuery
from loader import dp, db, bot
from aiogram import types
import logging


@dp.callback_query_handler(text_contains="menu")
async def open_menu(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text(f"Меню: ",
                                 reply_markup=menu_inline_kb)


@dp.callback_query_handler(text_contains="my_profile")
async def my_profile_menu(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    user = await db.select_user(telegram_id=call.from_user.id)

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
    #::::::::::::::::::::::::#
    #::::::::::::::::::::::::#
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
    usercomm = user.get('commentary')
    user_photo = user.get('photo_id')
    if user_photo:
        user_photo = user.get('photo_id')
    elif user_photo is None:
        user_photo = 'https://www.pngfind.com/pngs/m/110-1102775_download-empty-profile-hd-png-download.png'

    logging.info(f"{callback_data}=")
    await bot.send_photo(chat_id=call.from_user.id, caption=f'{str(username)}, {str(userage)}\n\n'
                                                            f'{usersex}, {str(usercity)}, {str(usernational)}\n\n'
                                                            f'{usereducation}\n'
                                                            f'{usercar}\n'
                                                            f'{userapart}\n'
                                                            f'{userkids}\n\n'
                                                            f'{userlifestyle}\n\n'
                                                            f'Обо мне: {str(usercomm)}',
                         photo=user_photo)


@dp.callback_query_handler(text_contains="preferences")
async def get_preferences(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data

    logging.info(f"{callback_data}=")
    await call.message.answer("Кого вы ищете? ", reply_markup=btn_pref)


@dp.callback_query_handler(text_contains="male")
async def get_male(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data

    logging.info(f"{callback_data}=")
    await db.update_user_need_partner_sex(need_partner_sex='Мужской', telegram_id=call.from_user.id)
    await call.message.edit_text("Вы выбрали мужчин", reply_markup=menu_inline_kb)


@dp.callback_query_handler(text_contains="g_fe")
async def get_male(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data

    logging.info(f"{callback_data}=")
    await db.update_user_need_partner_sex(need_partner_sex='Женский', telegram_id=call.from_user.id)
    await call.message.edit_text("Вы выбрали женщин", reply_markup=menu_inline_kb)


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    await call.message.edit_text(f"Рад был помочь, {call.from_user.full_name}!\n"
                                 f"Надеюсь, ты нашел кого-то благодаря мне", reply_markup=inline_start)
