from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from functions.get_data_func import get_data_meetings
from keyboards.inline.game_inline import game_keyboard
from keyboards.inline.sending_quest import moderate_keyboard
from loader import dp, _
from utils.db_api import db_commands


@dp.callback_query_handler(text="meetings")
async def pre_registration(call: CallbackQuery, state: FSMContext):
    user = await get_data_meetings(telegram_id=call.from_user.id)
    user_premium = user[5]
    if user[4] == "Одобрено" and not user_premium:
        await call.message.edit_text(_("Спасибо, что заполнили анкету,"
                                       " теперь у вас есть возможность приобрести подписку,"
                                       " а после с вами свяжется менеджер"),
                                     reply_markup=await game_keyboard(user_premium))
    elif user[4] != "Одобрено":
        await call.message.edit_text(_("Приветствую, вы перешли в раздел с поиском офлайн игр.\n"
                                       "Для поиска вам необходимо пройти опрос.\n\n"
                                       "Напишите, в какую игру вы бы хотели сыграть?"))
        await state.set_state("registration_game")
    if user_premium:
        await call.message.edit_text(_("Спасибо, что оплатили подписку, теперь вам нужно выбрать дату проведения игры"),
                                     reply_markup=await game_keyboard(user_premium))


@dp.message_handler(state="registration_game")
async def registration_level_game(message: types.Message, state: FSMContext):
    await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, level_game=message.text)
    await state.update_data(level_game=message.text)
    await message.answer(_("Напишите компанию, в которой вы работаете, если вы не работаете поставьте '-'"))
    await state.set_state("registration_position")


@dp.message_handler(state="registration_position")
async def registration_pos(message: types.Message, state: FSMContext):
    await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, company_name=message.text)
    await state.update_data(company_name=message.text)
    await message.answer(_("Напишите вашу должность"))
    await state.set_state("send_manager")


@dp.message_handler(state="send_manager")
async def send_manager_form(message: types.Message, state: FSMContext):
    await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, position_in_company=message.text)
    await state.update_data(position_in_company=message.text)
    await state.finish()
    user = await get_data_meetings(telegram_id=message.from_user.id)
    text = _("Ваша заявка готова\n\n"
             "Имя: @{user_0}\n"
             "Уровень игры: {user_3}\n"
             "Должность: {user_2}\n"
             "Компания: {user_1}\n").format(user_0=user[0], user_3=user[3], user_2=user[2], user_1=user[1])
    await message.answer(text, reply_markup=await moderate_keyboard(messages="many"))
