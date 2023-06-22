import asyncio
import pathlib
from typing import NoReturn, Union, Optional

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, InputFile, InlineKeyboardMarkup
from loguru import logger

from keyboards.inline.filters_inline import dating_filters_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from loader import _, bot
from utils.db_api import db_commands


async def choice_gender(call: CallbackQuery) -> None:
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


async def display_profile(call: CallbackQuery, markup) -> None:
    """
    Функция для отображения профиля пользователя
    """
    user = await db_commands.select_user(telegram_id=call.from_user.id)
    user_verification = "✅" if user["verification"] else "❌"
    user_info_template = "{}, {} лет, {} {}\n\n{}"
    text = user_info_template.format(user["varname"], user["age"], user["city"], user_verification,
                                     user["commentary"])
    text_2 = user_info_template.format(user["varname"], user["age"], user["city"], user_verification,
                                       user["commentary"]) + "\n\n<b>Инстаграм</b> - <code>{}</code>\n".format(
        user["instagram"])
    text_3 = user_info_template.format(user["varname"], user["age"], user["city"], user_verification, "")

    if user["voice_id"] is None and user["instagram"] is None:
        caption = text
    elif user["voice_id"] is None:
        caption = text_2
    elif user["voice_id"] and user["instagram"] is None:
        caption = text_3
        await call.message.answer_voice(user["voice_id"], caption=_("Описание вашей анкеты"))
    else:
        caption = text_2
        await call.message.answer_voice(user["voice_id"], caption=_("Описание вашей анкеты"))
    await call.message.answer_photo(caption=caption, photo=user["photo_id"], reply_markup=markup)


async def show_dating_filters(
        call: Optional[CallbackQuery] = None,
        message: Optional[types.Message] = None
) -> None:
    user_id = call.from_user.id if call else message.from_user.id
    user = await db_commands.select_user(telegram_id=user_id)
    markup = await dating_filters_keyboard()

    text = _("Фильтр по подбору партнеров:\n\n"
             "🚻 Необходимы пол партнера: {}\n"
             "🔞 Возрастной диапазон: {}-{} лет\n\n"
             "🏙️ Город партнера: {}").format(
        user.get("need_partner_sex"),
        user.get("need_partner_age_min"),
        user.get("need_partner_age_max"),
        user.get("need_city"),
    )
    if call:
        await call.message.edit_text(text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)


# TODO: Add type hint
async def registration_menu(call, scheduler, send_message_week, load_config, random) -> None:
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


async def finished_registration(state: FSMContext, telegram_id: int, message: types.Message) -> None:
    await state.finish()
    await db_commands.update_user_data(telegram_id=telegram_id, status=True)

    user = await db_commands.select_user(telegram_id=telegram_id)

    markup = await start_keyboard(status=user.get("status"))

    text = _(f"Регистрация успешно завершена! \n\n "
             "{}, "
             "{} лет, "
             "{}\n\n"
             "<b>О себе</b> - {}").format(user.get("varname"), user.get("age"),
                                          user.get("city"),
                                          user.get("commentary"))

    await message.answer_photo(caption=text,
                               photo=user.get('photo_id'), reply_markup=ReplyKeyboardRemove())
    await message.answer("Меню: ", reply_markup=markup)


async def saving_normal_photo(message: types.Message, telegram_id: int, file_id: int, state: FSMContext) -> None:
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
                                markup: Union[InlineKeyboardMarkup, None] = None) -> None:
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


async def update_normal_photo(
        message: types.Message,
        telegram_id: int,
        file_id: int,
        state: FSMContext,
        markup) -> None:
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
