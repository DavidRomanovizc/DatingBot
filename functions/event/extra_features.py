from datetime import datetime
from typing import List, NoReturn, Union

from aiogram.types import CallbackQuery

from functions.event.templates_messages import ME
from functions.main_app.get_data_func import get_data_meetings, get_data
from loader import bot
from utils.db_api import db_commands


async def add_events_to_user(call: CallbackQuery, event_id: int) -> NoReturn:
    """
    Функция, сохраняющая id мероприятий, которые лайкнул пользователь
    """
    user = await get_data(call.from_user.id)
    event_list = user[14]

    # noinspection PyTypeChecker
    if event_list.count(f"{event_id}") == 0:
        await db_commands.update_user_events(telegram_id=call.from_user.id, events_id=event_id)


async def check_availability_on_event() -> bool:
    """
    Функция, которая проверяет наличие свободных мест на мероприятие
    """
    ...


async def check_event_date(telegram_id: int) -> NoReturn:
    """
    Функция, которая проверяет - прошло мероприятие или нет
    """
    event = await get_data_meetings(telegram_id)
    date = datetime.strptime(event[3], '%d-%m-%Y')
    if date <= datetime.strptime((str(datetime.now()).split(" "))[0], '%Y-%m-%d'):
        await db_commands.update_user_meetings_data(telegram_id=telegram_id, is_admin=False)
        await db_commands.update_user_meetings_data(telegram_id=telegram_id, verification_status=False)
    else:
        await db_commands.update_user_meetings_data(telegram_id=telegram_id, is_active=True)


async def create_form(form_owner: int, chat_id: int, call: CallbackQuery, view: Union[bool, None] = True) -> NoReturn:
    """
    Функция, которая заполняет анкету текстом
    """
    owner = await get_data_meetings(telegram_id=form_owner)

    document = {
        "title": owner[2],
        "date": owner[3],
        "place": owner[4],
        "description": owner[1],
        "photo_id": owner[5],
        "telegram_id": form_owner
    }
    if view:
        await ME.send_event_message(text=document, bot=bot, chat_id=chat_id, view_event=True, call=call)
    else:
        await ME.send_event_list(text=document, call=call, bot=bot, telegram_id=call.from_user.id)


async def get_next_event(telegram_id: int) -> List[int]:
    """
    Функция, заполняющая список id пользователей, которые создали мероприятие и прошли модерацию
    """
    event = await db_commands.search_event_forms()
    event_list = []

    for i in event:
        if int(i['telegram_id']) != int(telegram_id):
            event_list.append(i['telegram_id'])

    return event_list
