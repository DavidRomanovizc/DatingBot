import asyncio
import datetime
import os
import pathlib
import random
import re
import shutil
from contextlib import suppress
from typing import Union, Optional

import aiofiles
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    ReplyKeyboardRemove,
    InputFile,
    InlineKeyboardMarkup,
    Message
)
from aiogram.utils.exceptions import (
    BadRequest,
    MessageCantBeDeleted,
    MessageToDeleteNotFound
)
from asyncpg import UniqueViolationError

from data.config import load_config
from functions.main_app.app_scheduler import send_message_week
from keyboards.inline.filters_inline import dating_filters_keyboard
from keyboards.inline.guide_inline import create_pagination_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.settings_menu import information_keyboard
from loader import (
    _,
    bot,
    scheduler
)
from utils.db_api import db_commands
from utils.db_api.db_commands import (
    check_user_exists,
    check_user_meetings_exists
)


async def delete_message(message: Message) -> None:
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


async def choice_gender(call: CallbackQuery) -> None:
    """
    Функция, сохраняющая в базу пол, который выбрал пользователь
    """
    sex_mapping = {
        'male': 'Мужской',
        'female': 'Женский'
    }

    selected_sex = sex_mapping.get(call.data)

    if selected_sex:
        try:
            await db_commands.update_user_data(
                telegram_id=call.from_user.id,
                need_partner_sex=selected_sex
            )
        except UniqueViolationError:
            pass


async def display_profile(call: CallbackQuery, markup: InlineKeyboardMarkup) -> None:
    """
    Функция для отображения профиля пользователя
    """
    user = await db_commands.select_user(telegram_id=call.from_user.id)
    count_referrals = await db_commands.count_all_users_kwarg(referrer_id=call.from_user.id)
    user_verification = "✅" if user["verification"] else ""

    user_info_template = _(
        "{name}, {age} лет, {city}, {verification}\n\n{commentary}\n\n"
        "<u>Партнерка:</u>\nКоличество приглашенных друзей: {reff}\nРеферальная ссылка:\n {link}"
    )
    info = await bot.get_me()
    user_info = user_info_template.format(
        name=user["varname"],
        age=user["age"],
        city=user["city"],
        verification=user_verification,
        commentary=user["commentary"],
        reff=count_referrals,
        link=f"https://t.me/{info.username}?start={call.from_user.id}"
    )

    await call.message.answer_photo(caption=user_info, photo=user["photo_id"], reply_markup=markup)


async def show_dating_filters(
        obj: Union[CallbackQuery, Message]
) -> None:
    user_id = obj.from_user.id
    user = await db_commands.select_user(telegram_id=user_id)
    markup = await dating_filters_keyboard()

    text = _(
        "Фильтр по подбору партнеров:\n\n"
        "🚻 Необходимы пол партнера: {}\n"
        "🔞 Возрастной диапазон: {}-{} лет\n\n"
        "🏙️ Город партнера: {}").format(
        user.get("need_partner_sex"),
        user.get("need_partner_age_min"),
        user.get("need_partner_age_max"),
        user.get("need_city"),
    )
    try:
        await obj.message.edit_text(text, reply_markup=markup)
    except AttributeError:
        await obj.answer(text, reply_markup=markup)


async def registration_menu(
        obj: Union[CallbackQuery, Message],
) -> None:
    support = await db_commands.select_user(telegram_id=load_config().tg_bot.support_ids[0])
    markup = await start_keyboard(obj)
    heart = random.choice(['💙', '💚', '💛', '🧡', '💜', '🖤', '❤', '🤍', '💖', '💝'])
    text = _("Приветствую вас, {fullname}!!\n\n"
             "{heart} <b> QueDateBot </b> - платформа для поиска новых знакомств.\n\n"
             "🪧 Новости о проекте вы можете прочитать в нашем канале - "
             "https://t.me/QueDateGroup \n\n"
             "<b>🤝 Сотрудничество: </b>\n"
             "Если у вас есть предложение о сотрудничестве, пишите агенту поддержки - "
             "@{supports}\n\n").format(fullname=obj.from_user.full_name, heart=heart,
                                       supports=support['username'])
    try:
        await obj.message.edit_text(
            text=text,
            reply_markup=markup
        )
        scheduler.add_job(
            send_message_week,
            trigger="interval",
            weeks=1,
            jitter=120,
            args={obj.message}
        )
    except AttributeError:
        await obj.answer(
            text=text,
            reply_markup=markup
        )
        scheduler.add_job(
            send_message_week,
            trigger="interval",
            weeks=1,
            jitter=120,
            args={obj}
        )
    except BadRequest:
        await delete_message(obj.message)

        await obj.message.answer(
            text=text,
            reply_markup=markup
        )


async def check_user_in_db(telegram_id: int, message: Message, username: str) -> None:
    if (
            not await check_user_exists(telegram_id) and
            not await check_user_meetings_exists(telegram_id)
    ):
        user = await db_commands.select_user_object(telegram_id=telegram_id)
        referrer_id = message.text[7:]
        if referrer_id != "" and referrer_id != telegram_id:
            await db_commands.add_user(
                name=message.from_user.full_name,
                telegram_id=telegram_id,
                username=username,
                referrer_id=referrer_id
            )
            await db_commands.update_user_data(
                telegram_id=telegram_id,
                limit_of_views=user.limit_of_views + 15
            )
            await bot.send_message(
                chat_id=referrer_id,
                text=_(
                    "По вашей ссылке зарегистрировался пользователь {}!\n"
                    "Вы получаете дополнительных 15 ❤️"
                ).format(
                    message.from_user.username
                )
            )
        else:
            await db_commands.add_user(
                name=message.from_user.full_name,
                telegram_id=telegram_id,
                username=username
            )
        await db_commands.add_meetings_user(telegram_id=telegram_id,
                                            username=username)
        if telegram_id in load_config().tg_bot.admin_ids:
            await db_commands.add_user_to_settings(telegram_id=telegram_id)


async def finished_registration(
        state: FSMContext,
        telegram_id: int,
        message: Message
) -> None:
    await state.finish()
    await db_commands.update_user_data(telegram_id=telegram_id, status=True)

    user = await db_commands.select_user(telegram_id=telegram_id)

    markup = await start_keyboard(obj=message)

    text = _("Регистрация успешно завершена! \n\n "
             "{}, "
             "{} лет, "
             "{}\n\n"
             "<b>О себе</b> - {}").format(user.get("varname"), user.get("age"),
                                          user.get("city"),
                                          user.get("commentary"))

    await message.answer_photo(caption=text,
                               photo=user.get('photo_id'), reply_markup=ReplyKeyboardRemove())
    await message.answer("Меню: ", reply_markup=markup)


async def saving_normal_photo(
        message: Message,
        telegram_id: int,
        file_id: int,
        state: FSMContext
) -> None:
    """
    Функция, сохраняющая фотографию пользователя без цензуры
    """
    try:
        await db_commands.update_user_data(
            telegram_id=telegram_id,
            photo_id=file_id
        )

        await message.answer(text=_("Фото принято!"))
    except:
        await message.answer(
            text=_("Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n"
                   "Если ошибка осталась, напишите агенту поддержки.")
        )
    await finished_registration(
        state=state,
        telegram_id=telegram_id,
        message=message
    )


async def saving_censored_photo(
        message: Message,
        telegram_id: int,
        state: FSMContext,
        out_path: Union[str, pathlib.Path],
        flag: Optional[str] = "registration",
        markup: Union[InlineKeyboardMarkup, None] = None
) -> None:
    """
    Функция, сохраняющая фотографию пользователя с цензурой
    """
    photo = InputFile(out_path)
    id_photo = await bot.send_photo(
        chat_id=telegram_id,
        photo=photo,
        caption=_(
            "Во время проверки вашего фото мы обнаружили подозрительный контент!\n"
            "Поэтому мы чуть-чуть подкорректировали вашу фотографию"
        )
    )
    file_id = id_photo['photo'][0]['file_id']
    await asyncio.sleep(1)
    try:
        await db_commands.update_user_data(
            telegram_id=telegram_id,
            photo_id=file_id
        )

    except Exception as err:
        await message.answer(
            text=_(
                "Произошла ошибка!"
                " Попробуйте еще раз либо отправьте другую фотографию. \n"
                "Если ошибка осталась, напишите агенту поддержки."
            )
        )
    if flag == "change_datas":
        await message.answer(
            text=_("Фото принято!"),
            reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(3)
        await message.answer(
            text=_("Выберите, что вы хотите изменить: "),
            reply_markup=markup
        )
        await state.reset_state()
    elif flag == "registration":
        await finished_registration(
            state=state,
            telegram_id=telegram_id,
            message=message
        )


async def update_normal_photo(
        message: Message,
        telegram_id: int,
        file_id: int,
        state: FSMContext,
        markup
) -> None:
    """
    Функция, которая обновляет фотографию пользователя
    """
    try:
        await db_commands.update_user_data(
            telegram_id=telegram_id,
            photo_id=file_id
        )
        await message.answer(
            text=_("Фото принято!"),
            reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(3)
        await message.answer(
            text=_("Выберите, что вы хотите изменить: "),
            reply_markup=markup
        )
        await state.reset_state()
    except:
        await message.answer(
            text=_(
                "Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n"
                "Если ошибка осталась, напишите агенту поддержки."
            )
        )


async def dump_users_to_file():
    async with aiofiles.open("users.txt", "w", encoding='utf-8') as file:
        _text = ""
        _users = await db_commands.select_all_users()
        for user in _users:
            _text += str(user) + "\n"

        await file.write(_text)

    return "users.txt"


async def backup_configs():
    shutil.make_archive("backup_data", 'zip', "./logs/")
    return "./backup_data.zip"


async def send_photo_with_caption(
        call: CallbackQuery,
        photo: str,
        caption: str,
        step: int,
        total_steps: int,
) -> None:
    markup = await create_pagination_keyboard(step, total_steps)

    await call.message.delete()
    await call.message.answer_photo(types.InputFile(photo), reply_markup=markup, caption=caption)


async def handle_guide_callback(
        call: CallbackQuery,
        callback_data: dict,
) -> None:
    step = int(callback_data.get("value"))

    photo_path = f"brandbook/{step}_page.png"
    caption = _("Руководство по боту: \n<b>Страница №{}</b>").format(step)
    await send_photo_with_caption(
        call=call,
        photo=photo_path,
        caption=caption,
        step=step,
        total_steps=len(os.listdir("brandbook/"))
    )


async def information_menu(call: CallbackQuery):
    start_date = datetime.datetime(2021, 8, 10, 14, 0)
    now_date = datetime.datetime.now()
    delta = now_date - start_date
    count_users = await db_commands.count_users()
    markup = await information_keyboard()
    txt = _("Вы попали в раздел <b>Информации</b> бота, здесь вы можете посмотреть: статистику,"
            "изменить язык, а также посмотреть наш брендбук.\n\n"
            "🌐 Дней работаем: <b>{}</b>\n"
            "👤 Всего пользователей: <b>{}</b>\n").format(delta.days, count_users)
    try:
        await call.message.edit_text(
            text=txt,
            reply_markup=markup
        )
    except BadRequest:
        await delete_message(call.message)
        await call.message.answer(
            text=txt,
            reply_markup=markup
        )


async def get_report_reason(call: CallbackQuery):
    match = re.search(r'report:(.*?):', call.data)
    reason_key = match.group(1)
    reason_mapping = {
        "adults_only": "🔞 Развратный контент",
        "drugs": "💊 Продажа наркотиков",
        "scam": "💰 Мошенничество",
        "another": "🦨 Другая причина"
    }
    return reason_mapping.get(reason_key, "Неизвестная причина")
