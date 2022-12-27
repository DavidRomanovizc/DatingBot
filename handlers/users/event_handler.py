import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType
from loguru import logger

from functions.auxiliary_tools import determining_location
from functions.get_data_func import get_data_meetings
from functions.templates_messages import ME
from keyboards.inline.calendar import calendar_callback, SimpleCalendar
from keyboards.inline.poster_inline import poster_keyboard
from loader import dp, _, bot
from utils.db_api import db_commands


@dp.callback_query_handler(text="meetings")
async def view_meetings_handler(call: CallbackQuery):
    user = await get_data_meetings(call.from_user.id)
    is_admin = user[-1]
    await call.message.edit_text(_("Вы перешли в меню афиш"), reply_markup=await poster_keyboard(is_admin))


@dp.callback_query_handler(text="create_poster")
async def registrate_poster_name(call: CallbackQuery, state: FSMContext):
    user = await get_data_meetings(call.from_user.id)
    is_admin = user[-1]
    try:
        user = await get_data_meetings(call.from_user.id)
        moderation_process = user[8]
        if moderation_process:
            await call.message.edit_text(_("Введите название мероприятие"))
            await state.set_state("register_handler_name")
        else:
            await call.message.edit_text(
                "Вы уже создали мероприятие, которое проходит модерацию. Дождитесь проверки, пожалуйста",
                reply_markup=await poster_keyboard(is_admin))
    except AttributeError:
        if call.from_user.username is not None:
            await db_commands.add_meetings_user(telegram_id=call.from_user.id,
                                                username=call.from_user.username)
        else:
            await db_commands.add_meetings_user(telegram_id=call.from_user.id,
                                                username="None")
        await call.message.edit_text(_("Произошла ошибка, попробуйте еще раз"),
                                     reply_markup=await poster_keyboard(is_admin))


@dp.message_handler(state="register_handler_name")
async def simple_calendar(message: Message):
    try:
        await message.answer(_("Пожалуйста, выберите дату: "),
                             reply_markup=await SimpleCalendar().start_calendar())
        await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, event_name=message.text)
    except:
        pass


@dp.callback_query_handler(calendar_callback.filter(), state="register_handler_name")
async def process_simple_calendar(call: CallbackQuery, callback_data, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    now = datetime.datetime.now()

    if now.strftime("%d-%m-%Y") > date.strftime("%d-%m-%Y"):
        await call.message.edit_text("Вы не можете проводить мероприятие в прошлом")
        await simple_calendar(call.message)
        return
    if selected:
        await call.message.edit_text(_("Теперь напишите место проведения"))
        await db_commands.update_user_meetings_data(telegram_id=call.from_user.id, time_event=date.strftime("%d-%m-%Y"))
    else:
        return
    await state.set_state("register_handler_place")


@dp.message_handler(state="register_handler_place")
async def send_city(message: types.Message):
    try:
        await determining_location(message, event=True)
    except Exception as err:
        await message.answer(_("Произошла неизвестная ошибка! Попробуйте еще раз.\n"
                               "Вероятнее всего вы ввели город неправильно"))
        logger.error(err)


@dp.callback_query_handler(text="yes_all_good", state="register_handler_place")
async def registrate_poster_commentary(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text(_("Хорошо, теперь напишите короткое или длинное описание вашего мероприятия"))
    except Exception as err:
        logger.info(err)
    await state.set_state("register_handler_commentary")


@dp.message_handler(state="register_handler_commentary")
async def registrate_poster_commentary(message: Message, state: FSMContext):
    try:
        await message.answer(_("И напоследок, пришлите постер вашего мероприятия"))
        await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, commentary=message.text)
    except Exception as err:
        logger.info(err)
    await state.set_state("register_handler_poster")


@dp.message_handler(content_types=ContentType.PHOTO, state="register_handler_poster")
async def finish_registration(message: Message, state: FSMContext):
    user = await get_data_meetings(message.from_user.id)
    is_admin = user[-1]
    photo_id = message.photo[-1].file_id
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, photo_id=photo_id)
        await message.answer(_("Фото принято"))
    except Exception as err:
        logger.info(err)
        await message.answer(_("Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n"
                               "Если ошибка осталась, напишите агенту поддержки."))
    await state.finish()
    user = await get_data_meetings(telegram_id=message.from_user.id)

    document = {
        "title": user[2],
        "date": user[3],
        "place": user[4],
        "description": user[1],
        "photo_id": photo_id,
        "telegram_id": message.from_user.id
    }
    await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, moderation_process=False)
    await ME.send_moderate_message(text=document, bot=bot)
    await message.answer(_("Ваше мероприятие отправлено на модерацию"), reply_markup=await poster_keyboard(is_admin))
