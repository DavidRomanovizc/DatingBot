from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.menu_profile_inline import get_profile
from keyboards.inline.second_menu_inline import second_menu_keyboard
from handlers.users.back_handler import delete_message

from utils.db_api import db_commands
from loader import dp
from utils.misc.create_questionnaire import get_data


@dp.callback_query_handler(text="second_m")
async def open_menu(call: CallbackQuery):
    markup = await second_menu_keyboard()
    await call.message.edit_text(f"<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                                 f"<b>🤝 Сотрудничество: </b>\n"
                                 f"Если у вас есть предложение о сотрудничестве, пишите сюда - "
                                 f"@borisLobkov\n\n",
                                 reply_markup=markup)


@dp.callback_query_handler(text="my_profile")
async def my_profile_menu(call: CallbackQuery):
    await delete_message(call.message)
    markup = await get_profile()
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)

    await call.message.answer_photo(caption=f"Ваша анкета:\n\n "
                                            f"<b>Статус анкеты</b> - \n{str(user_data[6])}\n\n"
                                            f"<b>Имя</b> - {str(user_data[0])}\n"
                                            f"<b>Возраст</b> - {str(user_data[1])}\n"
                                            f"<b>Пол</b> - {str(user_data[2])}\n"
                                            f"<b>Город</b> - {str(user_data[3])}\n"
                                            f"<b>Ваше занятие</b> - {str(user_data[4])}\n\n"
                                            f"<b>О себе</b> - {str(user_data[5])}\n",
                                    photo=user_data[7], reply_markup=markup)


# TODO: Написать отключение анкеты. Для начала нужно написать методы в бд
@dp.callback_query_handler(text="disable")
async def disable_profile(call: CallbackQuery):
    await call.answer("Coming soon...")
