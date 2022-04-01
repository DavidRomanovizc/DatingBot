from aiogram.types import CallbackQuery
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp, db
from utils.db_api import db_commands


@dp.callback_query_handler(text="statistics")
async def get_inst(call: CallbackQuery):
    markup = await start_keyboard()
    count_users = await db_commands.count_users()
    await call.message.edit_text(f"<b>💻 Статистика: </b>\n\n"
                                 f"└Сейчас в нашем боте <b>{count_users} пользователей</b>"
                                 f"└Дата создания бота - <b>10.08.2021</b>", reply_markup=markup
                                 )
