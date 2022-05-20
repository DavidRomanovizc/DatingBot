from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.back_inline import only_back_keyboard
from keyboards.inline.meeting_inline import meeting_keyboard
from loader import dp
from utils.db_api import db_commands
from utils.misc.create_questionnaire import get_data, get_meeting_data


@dp.callback_query_handler(text="meetings")
async def meetings_menu_handler(call: CallbackQuery):
    user_data = await get_data(call.from_user.id)
    if user_data[6] == "✅ Подтвержденный":
        await call.message.edit_text("Вы перешли в меню тусовок", reply_markup=await meeting_keyboard())
    else:
        await call.answer("Пожалуйста, пройдите верификацию, а потом возвращайтесь")


@dp.callback_query_handler(text="create_ques")
async def create_ques(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Приветствую, вы должны написать описание к своему мероприятию, например:\n\n"
                                 "Традиционные завтраки каждый вторник\n"
                                 "<b>Что делаем:</b>\n"
                                 "- Знакомимся, завтракаем, пьем кофе\n"
                                 "- Рассказываем кулстори из жизни и работы\n"
                                 "<b>Время:</b>\n Вторник, начинаем в 9:30\n"
                                 "<b>Место:</b>\n Манежный пер Санкт-Петербург Cake & Breakfast")
    await state.set_state("fill_ques")


@dp.message_handler(state="fill_ques")
async def fill_questionary(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    await db_commands.update_user_meetings_data(telegram_id=telegram_id, meetings_description=message.text)
    await state.finish()

    user_data = await get_meeting_data(telegram_id)

    await message.answer("<b>Мероприятие создано!</b>\n\n"
                         f"{user_data[1]}\n\n"
                         f'<a href="https://t.me/{user_data[0]}">{user_data[0]}</a>',
                         reply_markup=await only_back_keyboard())