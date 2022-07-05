from aiogram.types import CallbackQuery

from handlers.users.back_handler import delete_message
from keyboards.inline.menu_profile_inline import get_profile_keyboard
from loader import dp
from utils.db_api import db_commands
from functions.get_data_func import get_data


@dp.callback_query_handler(text="my_profile")
async def my_profile_menu(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    await delete_message(call.message)
    user_db = await db_commands.select_user(telegram_id=telegram_id)
    markup = await get_profile_keyboard(verification=user_db["verification"])
    await call.message.answer_photo(caption=f"<b>Ваша анкета:</b>\n\n"
                                            f"{str(user_data[0])}, "
                                            f"{str(user_data[1])} лет, "
                                            f"{str(user_data[3])}\n\n"
                                            f"<b>О себе</b> - {str(user_data[5])}\n\n"
                                            f"<b>Инстаграм</b> - <code>{str(user_data[8])}</code>\n"
                                            f"<b>Статус анкеты - {str(user_data[6])}</b>",
                                    photo=user_data[7], reply_markup=markup)


@dp.callback_query_handler(text="disable")
async def disable_profile(call: CallbackQuery):
    await db_commands.delete_user(telegram_id=call.from_user.id)
    await delete_message(call.message)
    await call.message.answer("Ваша анкета удалена!\nЯ надеюсь вы кого-нибудь нашли")
