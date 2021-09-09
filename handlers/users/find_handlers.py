from keyboards.inline.questionnaires_inline import questionnaires_inline_kb
from aiogram.types import CallbackQuery
from loader import dp, bot


@dp.callback_query_handler(text='start_finder')
async def start_finder(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'здесь будут появлятся анкеты других '
                                                        f'людей с такими кнопками',
                           reply_markup=questionnaires_inline_kb)