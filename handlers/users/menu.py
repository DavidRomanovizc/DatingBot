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
                                 f"@DRomanovizc\n\n",
                                 reply_markup=markup)


@dp.callback_query_handler(text="my_profile")
async def my_profile_menu(call: CallbackQuery):
    await delete_message(call.message)
    markup = await get_profile()
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    user = await db_commands.select_user(telegram_id=telegram_id)
    await call.message.answer_photo(caption=f"Ваша анкета:\n\n "
                                            f"Статус анкеты - {str(user_data[12])}\n\n"
                                            f"1. Ваше имя - {str(user_data[0])}\n"
                                            f"2. Ваш возраст - {str(user_data[1])}\n"
                                            f"3. Ваш пол - {str(user_data[2])}\n"
                                            f"4. Ваша национальность - {str(user_data[3])}\n"
                                            f"5. Ваше образование - {str(user_data[4])}\n"
                                            f"6. Ваш город - {str(user_data[5])}\n"
                                            f"7. Наличие машины - {str(user_data[6])}\n"
                                            f"8. Наличие жилья - {str(user_data[7])}\n"
                                            f"9. Ваше занятие - {str(user_data[8])}\n"
                                            f"10. Наличие детей - {str(user_data[9])}\n"
                                            f"11. Семейное положение - {str(user_data[10])}\n\n"
                                            f"12. О себе - {str(user_data[11])}\n\n",
                                    photo=user.get('photo_id'), reply_markup=markup)


# TODO: Написать отключение анкеты. Для начала нужно написать методы в бд
@dp.callback_query_handler(text="disable")
async def disable_profile(call: CallbackQuery):
    await call.answer("Coming soon...")
