from aiogram.types import CallbackQuery

from keyboards.inline.back_bnt import go_back_to_the_menu
from loader import dp


@dp.callback_query_handler(text_contains="instruction")
async def get_inst(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text(f"<b>Инструкция: </b>\n\n"
                                 f"<b>1. Навигация по анкетам\n\n</b>"
                                 f"👍 - <i>вам понравилась анкета другого пользователя</i>\n"
                                 f"👎 - <i>вам не понравилась анкета</i>\n"
                                 f"💌 - <i>отправить через бота сообщение</i>\n"
                                 f"🛑 - <i>пожаловаться на анкету/пользователя</i>\n\n"
                                 f"Если вы нашли баг, то можете сообщить нам, написав сюда\n - @DRomanovizc или "
                                 f"@mroshalom",
                                 reply_markup=go_back_to_the_menu)
