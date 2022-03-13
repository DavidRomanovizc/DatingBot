from keyboards.inline.questionnaires_inline import questionnaires_inline_kb
from aiogram.types import CallbackQuery
from loader import dp, bot


@dp.callback_query_handler(text='start_finder')
async def start_finder(call: CallbackQuery):
    await call.message.edit_text('здесь будут появляться анкеты других '
                                 f'людей с такими кнопками',
                                 reply_markup=questionnaires_inline_kb)
