import asyncio
import pathlib
from typing import NoReturn, Union

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, InputFile, InlineKeyboardMarkup
from loguru import logger

from functions.dating.get_data_filters_func import get_data_filters
from functions.main_app.get_data_func import get_data
from keyboards.inline.filters_inline import dating_filters_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from loader import _, bot
from utils.db_api import db_commands


async def choice_gender(call: CallbackQuery) -> NoReturn:
    """
    Функция, сохраняющая в базу пол, который выбрал пользователь
    """
    if call.data == 'male':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, need_partner_sex='Мужской')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'female':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, need_partner_sex='Женский')
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)


async def display_profile(call: CallbackQuery, markup) -> NoReturn:
    """
    Функция для отображения профиля пользователя
    """
    user_data = await get_data(call.from_user.id)
    text = _("{user_0}, "
             "{user_1} лет, "
             "{user_3} {user_6}\n\n"
             "{user_5}").format(user_0=str(user_data[0]), user_1=str(user_data[1]),
                                user_3=str(user_data[3]),
                                user_5=str(user_data[5]),
                                user_6=str(user_data[6]),
                                )
    text_2 = _("{user_0}, "
               "{user_1} лет, "
               "{user_3} {user_6}\n\n"
               "{user_5}\n\n"
               "<b>Инстаграм</b> - <code>{user_8}</code>\n").format(user_0=str(user_data[0]),
                                                                    user_1=str(user_data[1]),
                                                                    user_3=str(user_data[3]),
                                                                    user_5=str(user_data[5]),
                                                                    user_6=str(user_data[6]),
                                                                    user_8=str(user_data[8]))
    text_3 = _("{user_0}, "
               "{user_1} лет, "
               "{user_3} {user_6}\n\n").format(user_0=str(user_data[0]),
                                               user_1=str(user_data[1]),
                                               user_3=str(user_data[3]),
                                               user_6=str(user_data[6]))
    if user_data[11] is None and user_data[8] == "Пользователь не прикрепил Instagram":
        await call.message.answer_photo(caption=text, photo=user_data[7], reply_markup=markup)
    elif user_data[11] is None:
        await call.message.answer_photo(caption=text_2,
                                        photo=user_data[7], reply_markup=markup)
    elif user_data[11] and user_data[8] == "Пользователь не прикрепил Instagram":
        await call.message.answer_photo(caption=text_3,
                                        photo=user_data[7], reply_markup=markup)
        await call.message.answer_voice(user_data[11], caption=_("Описание вашей анкеты"))
    else:
        await call.message.answer_photo(caption=text_2,
                                        photo=user_data[7], reply_markup=markup)
        await call.message.answer_voice(user_data[11], caption=_("Описание вашей анкеты"))


async def show_dating_filters(call: Union[CallbackQuery, None], message: Union[types.Message, None]):
    if message is None:
        user_data = await get_data_filters(call.from_user.id)

        text = _("Фильтр по подбору партнеров:\n\n"
                 "🚻 Необходимы пол партнера: {user_2}\n"
                 "🔞 Возрастной диапазон: {user_0}-{user_1} лет\n\n"
                 "🏙️ Город партнера: {user_3}").format(
            user_2=user_data[2],
            user_0=user_data[0],
            user_1=user_data[1],
            user_3=user_data[3]
        )
        await call.message.edit_text(text,
                                     reply_markup=await dating_filters_keyboard())
    if call is None:
        user_data = await get_data_filters(message.from_user.id)
        text = _("Фильтр по подбору партнеров:\n\n"
                 "🚻 Необходимы пол партнера: {user_2}\n"
                 "🔞 Возрастной диапазон: {user_0}-{user_1} лет\n\n"
                 "🏙️ Город партнера: {user_3}").format(
            user_2=user_data[2],
            user_0=user_data[0],
            user_1=user_data[1],
            user_3=user_data[3]
        )
        await message.answer(text,
                             reply_markup=await dating_filters_keyboard())


async def registration_menu(call, scheduler, send_message_week, load_config, random):
    """

    """
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    support = await db_commands.select_user(telegram_id=load_config().tg_bot.support_ids[0])
    markup = await start_keyboard(user_db["status"])
    heart = random.choice(['💙', '💚', '💛', '🧡', '💜', '🖤', '❤', '🤍', '💖', '💝'])
    await call.message.edit_text(_("Приветствую вас, {fullname}!!\n\n"
                                   "{heart} <b> QueDateBot </b> - платформа для поиска новых знакомств.\n\n"
                                   "🪧 Новости о проекте вы можете прочитать в нашем канале - "
                                   "https://t.me/QueDateGroup \n\n"
                                   "<b>🤝 Сотрудничество: </b>\n"
                                   "Если у вас есть предложение о сотрудничестве, пишите агенту поддержки - "
                                   "@{supports}\n\n").format(fullname=call.from_user.full_name, heart=heart,
                                                             supports=support['username']),
                                 reply_markup=markup)
    scheduler.add_job(send_message_week, trigger="interval", weeks=3, jitter=120, args={call.message})


async def finished_registration(state: FSMContext, telegram_id: int, message: types.Message):
    """

    """
    await state.finish()
    await db_commands.update_user_data(telegram_id=telegram_id, status=True)
    user_data = await get_data(telegram_id)
    user_db = await db_commands.select_user(telegram_id=telegram_id)
    markup = await start_keyboard(status=user_db['status'])

    text = _(f"Регистрация успешно завершена! \n\n "
             "{user_0}, "
             "{user_1} лет, "
             "{user_3}\n\n"
             "<b>О себе</b> - {user_5}").format(user_0=str(user_data[0]), user_1=str(user_data[1]),
                                                user_3=str(user_data[3]),
                                                user_5=str(user_data[5]))

    await message.answer_photo(caption=text,
                               photo=user_db.get('photo_id'), reply_markup=ReplyKeyboardRemove())
    await message.answer("Меню: ", reply_markup=markup)


async def saving_normal_photo(message: types.Message, telegram_id: int, file_id: int, state: FSMContext):
    """
    Функция, сохраняющая фотографию пользователя без цензуры
    """
    try:
        await db_commands.update_user_data(telegram_id=telegram_id, photo_id=file_id)

        await message.answer(_("Фото принято!"))
    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n"
                               "Если ошибка осталась, напишите агенту поддержки."))
    await finished_registration(state, telegram_id, message)


async def saving_censored_photo(message: types.Message, telegram_id: int, state: FSMContext,
                                out_path: Union[str, pathlib.Path], flag: Union[str, None] = "registration",
                                markup: Union[InlineKeyboardMarkup, None] = None):
    """
    Функция, сохраняющая фотографию пользователя с цензурой
    """
    photo = InputFile(out_path)
    id_photo = await bot.send_photo(chat_id=telegram_id,
                                    photo=photo,
                                    caption=_("Во время проверки вашего фото мы обнаружили подозрительный контент!\n"
                                              "Поэтому мы чуть-чуть подкорректировали вашу фотографию"))
    file_id = id_photo['photo'][0]['file_id']
    await asyncio.sleep(1)
    try:
        await db_commands.update_user_data(telegram_id=telegram_id, photo_id=file_id)

    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n"
                               "Если ошибка осталась, напишите агенту поддержки."))
    if flag == "change_datas":
        await message.answer(_("Фото принято!"), reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(3)
        await message.answer(_("Выберите, что вы хотите изменить: "), reply_markup=markup)
        await state.reset_state()
    elif flag == "registration":
        await finished_registration(state, telegram_id, message)


async def update_normal_photo(message: types.Message, telegram_id: int, file_id: int, state: FSMContext,
                              markup):
    """
    Функция, которая обновляет фотографию пользователя
    """
    try:
        await db_commands.update_user_data(telegram_id=telegram_id, photo_id=file_id)
        await message.answer(_("Фото принято!"), reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(3)
        await message.answer(_("Выберите, что вы хотите изменить: "), reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(_("Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n"
                               "Если ошибка осталась, напишите агенту поддержки."))
