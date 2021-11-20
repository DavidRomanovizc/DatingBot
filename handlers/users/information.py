from aiogram.types import CallbackQuery

from keyboards.inline.back_bnt import go_back_to_the_menu
from loader import dp


@dp.callback_query_handler(text_contains="info")
async def information(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text("<b>Made by: </b>\n"
                                 "\n"
                                 "@DRomanovizc - Python Developer\n"
                                 "@mroshalom - Python Developer\n"
                                 "\n"
                                 "ПОЛЬЗУЯСЬ БОТОМ ВЫ АВТОМАТИЧЕСКИ СОГЛАШАЕТЕСЬ НА ОБРАБОТКУ ПЕРСОНАЛЬНЫХ ДАННЫХ\n"
                                 "<i>Dslango© 2021</i>",
                                 reply_markup=go_back_to_the_menu)


