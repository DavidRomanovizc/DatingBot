import asyncio

from aiogram.types import CallbackQuery

from handlers.users.back_handler import delete_message, hearts
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.menu_profile_inline import get_profile_keyboard
from keyboards.inline.registration_inline import registration_keyboard
from keyboards.inline.second_menu_inline import second_menu_keyboard
from loader import dp
from utils.db_api import db_commands
from utils.misc.create_questionnaire import get_data


@dp.callback_query_handler(text="second_m")
async def open_menu(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    user_status = user_data[9]
    if user_status:
        markup = await second_menu_keyboard()
        await call.message.edit_text(f"<b>{hearts[4]}️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                                     f"<b>🤝 Сотрудничество: </b>\n"
                                     f"Если у вас есть предложение о сотрудничестве, пишите сюда - "
                                     f"@Support\n\n",
                                     reply_markup=markup)
    else:
        await call.message.edit_text("Вам необходимо зарегистрироваться, нажмите на кнопку ниже",
                                     reply_markup=await registration_keyboard())


@dp.callback_query_handler(text="my_profile")
async def my_profile_menu(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    await delete_message(call.message)
    markup = await get_profile_keyboard()
    await call.message.answer_photo(caption=f"<b>Ваша анкета:</b>\n\n "
                                            f"<b>Статус анкеты</b> - \n{str(user_data[6])}\n\n"
                                            f"<b>Имя</b> - {str(user_data[0])}\n"
                                            f"<b>Возраст</b> - {str(user_data[1])}\n"
                                            f"<b>Пол</b> - {str(user_data[2])}\n"
                                            f"<b>Город</b> - {str(user_data[3])}\n"
                                            f"<b>Ваше занятие</b> - {str(user_data[4])}\n\n"
                                            f"<b>О себе</b> - {str(user_data[5])}\n"
                                            f"<b>Инстаграм</b> - <code>{str(user_data[8])}</code>\n",
                                    photo=user_data[7], reply_markup=markup)


@dp.callback_query_handler(text="disable")
async def disable_profile(call: CallbackQuery):
    await db_commands.delete_user(telegram_id=call.from_user.id)
    await delete_message(call.message)
    await call.message.answer("Ваша анкета удалена!\nЯ надеюсь вы кого-нибудь нашли")