import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound
from loguru import logger

from data.config import load_config
from functions.event.extra_features import check_event_date
from functions.event.templates_messages import ME
from functions.main_app.determin_location import Location
from functions.main_app.get_data_func import get_data_meetings
from keyboards.inline.calendar import calendar_callback, SimpleCalendar, search_cb
from keyboards.inline.poster_inline import poster_keyboard, cancel_registration_keyboard
from loader import dp, _, bot
from utils.db_api import db_commands


@dp.callback_query_handler(text="meetings")
async def view_meetings_handler(call: CallbackQuery):
    try:
        await check_event_date(call.from_user.id)
    except TypeError:
        pass
    user = await get_data_meetings(call.from_user.id)
    is_admin = user[10]
    is_verification = user[6]
    text = _("Вы перешли в меню афиш")
    try:
        await call.message.edit_text(text, reply_markup=await poster_keyboard(is_admin, is_verification))
    except MessageToEditNotFound:
        await call.message.answer(text, reply_markup=await poster_keyboard(is_admin, is_verification))


@dp.callback_query_handler(text="create_poster")
async def registrate_poster_name(call: CallbackQuery, state: FSMContext):
    user = await get_data_meetings(call.from_user.id)
    is_admin = user[10]
    is_verification = user[6]
    moderation_process = user[8]
    try:
        # TODO: Проверить как это работает
        if moderation_process:
            await call.message.edit_text(_("Введите название мероприятие"),
                                         reply_markup=await cancel_registration_keyboard())
            await state.set_state("register_handler_name")
        else:
            try:
                await call.message.edit_text(
                    "Вы уже создали мероприятие, которое проходит модерацию. Дождитесь проверки, пожалуйста",
                    reply_markup=await poster_keyboard(is_admin, is_verification))
            except MessageNotModified:
                await call.answer(
                    _("Прочитайте сообщение и не нажимайте на кнопку, пока ваше мероприятие не пройдет модерацию"),
                    show_alert=True)
    except AttributeError:
        if call.from_user.username is not None:
            await db_commands.add_meetings_user(telegram_id=call.from_user.id,
                                                username=call.from_user.username)
        else:
            await db_commands.add_meetings_user(telegram_id=call.from_user.id,
                                                username="None")
        await call.message.edit_text(_("Произошла ошибка, попробуйте еще раз"),
                                     reply_markup=await poster_keyboard(is_admin, is_verification))


@dp.message_handler(state="register_handler_name")
async def simple_calendar(message: Message):
    await message.answer(_("Пожалуйста, выберите дату: "),
                         reply_markup=await SimpleCalendar().start_calendar())
    await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, event_name=message.text)


@dp.callback_query_handler(calendar_callback.filter(), state="register_handler_name")
async def process_simple_calendar(call: CallbackQuery, callback_data, state: FSMContext):
    try:
        selected, date = await SimpleCalendar().process_selection(call, callback_data)
        now = datetime.datetime.now()

        if now > date:
            await call.message.edit_text("Вы не можете проводить мероприятие в прошлом")
            await simple_calendar(call.message)
            return
        if selected:
            await call.message.edit_text(_("Теперь напишите место проведения"),
                                         reply_markup=await cancel_registration_keyboard())
            await db_commands.update_user_meetings_data(telegram_id=call.from_user.id,
                                                        time_event=date.strftime("%d-%m-%Y"))
        else:
            return
        await state.set_state("register_handler_place")
    except Exception as err:
        logger.info(err)
        pass


@dp.message_handler(state="register_handler_place")
async def send_city(message: types.Message):
    try:
        loc = await Location(message=message)
        await loc.det_loc_in_event(message)
    except Exception as err:
        await message.answer(_("Произошла неизвестная ошибка! Попробуйте еще раз.\n"
                               "Вероятнее всего вы ввели город неправильно"))
        logger.error(err)


@dp.callback_query_handler(text="yes_all_good", state="register_handler_place")
async def registrate_poster_commentary(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text(_("Хорошо, теперь напишите короткое или длинное описание вашего мероприятия"),
                                     reply_markup=await cancel_registration_keyboard())
    except Exception as err:
        logger.info(err)
    await state.set_state("register_handler_commentary")


@dp.message_handler(state="register_handler_commentary")
async def registrate_poster_commentary(message: Message, state: FSMContext):
    try:
        await message.answer(_("И напоследок, пришлите постер вашего мероприятия"),
                             reply_markup=await cancel_registration_keyboard())
        await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, commentary=message.text)
    except Exception as err:
        logger.info(err)
    await state.set_state("register_handler_poster")


@dp.message_handler(content_types=ContentType.PHOTO, state="register_handler_poster")
async def finish_registration(message: Message, state: FSMContext):
    user = await get_data_meetings(message.from_user.id)
    is_admin = user[10]
    is_verification = user[6]
    photo_id = message.photo[-1].file_id

    await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, photo_id=photo_id)
    await message.answer(_("Фото принято"))

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
    await ME.send_event_message(text=document, bot=bot, chat_id=load_config().tg_bot.moderate_chat, moderate=True)
    await message.answer(_("Ваше мероприятие отправлено на модерацию"),
                         reply_markup=await poster_keyboard(is_admin, is_verification))


@dp.callback_query_handler(text="my_event")
async def view_own_event(call: CallbackQuery):
    user = await get_data_meetings(telegram_id=call.from_user.id)

    document = {
        "title": user[2],
        "date": user[3],
        "place": user[4],
        "description": user[1],
        "photo_id": user[5],
    }
    await ME.send_event_message(text=document, bot=bot, chat_id=call.from_user.id, moderate=False,
                                call=call)


@dp.callback_query_handler(search_cb.filter(action=["cancel"]), state="register_handler_name")
@dp.callback_query_handler(text="cancel_registration", state="register_handler_name")
@dp.callback_query_handler(text="cancel_registration", state="register_handler_poster")
@dp.callback_query_handler(text="cancel_registration", state="register_handler_place")
@dp.callback_query_handler(text="cancel_registration", state="register_handler_commentary")
async def cancel_register_poster_name(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await view_meetings_handler(call)
