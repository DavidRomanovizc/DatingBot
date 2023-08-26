from datetime import datetime
from typing import Union, Optional, List

from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import BadRequest

from functions.event.templates_messages import ME
from loader import bot, _
from utils.db_api import db_commands


async def add_events_to_user(call: CallbackQuery, event_id: int) -> None:
    """
    Функция, сохраняющая id мероприятий, которые лайкнул пользователь
    """
    user = await db_commands.select_user(telegram_id=call.from_user.id)
    event_list = user.get("events", [])

    if str(event_id) not in event_list:
        await db_commands.update_user_events(
            telegram_id=call.from_user.id, events_id=event_id
        )


async def check_availability_on_event() -> bool:
    """
    Функция, которая проверяет наличие свободных мест на мероприятие
    """
    ...


async def check_event_date(telegram_id: int) -> None:
    """
    Функция, которая проверяет - прошло мероприятие или нет
    """
    event = await db_commands.select_user_meetings(telegram_id)
    event_time = event.get("time_event")
    if event_time is None:
        return
    event_datetime, now_datetime = (
        datetime.strptime(event_time, "%d-%m-%Y"),
        datetime.now().date(),
    )
    is_admin = True
    verification_status = True
    is_active = True

    if event_datetime.date() <= now_datetime:
        is_admin = False
        verification_status = False
        is_active = False
    await db_commands.update_user_meetings_data(
        telegram_id=telegram_id,
        is_admin=is_admin,
        verification_status=verification_status,
        is_active=is_active,
    )


async def create_form(
        form_owner: int, chat_id: int, call: CallbackQuery, view: Union[bool, None] = True
) -> None:
    """
    Функция, которая заполняет анкету текстом
    """
    try:
        owner = await db_commands.select_user_meetings(telegram_id=form_owner)
        document = {
            "title": owner.get("event_name"),
            "date": owner.get("time_event"),
            "place": owner.get("venue"),
            "description": owner.get("commentary"),
            "photo_id": owner.get("photo_id"),
            "telegram_id": form_owner,
        }
        if view:
            await ME.send_event_message(
                text=document, bot=bot, chat_id=chat_id, view_event=True, call=call
            )
        else:
            await ME.send_event_list(
                text=document, call=call, bot=bot, telegram_id=call.from_user.id
            )
    except BadRequest:
        await call.answer(
            text=_("На данный момент у нас нет подходящих мероприятий для вас"),
            show_alert=True,
        )


async def get_next_random_event_id(telegram_id: int) -> Optional[int]:
    """
    Функция, возвращающая случайный id мероприятия, созданного другим пользователем
    """
    event_ids = await db_commands.search_event_forms()

    other_events_ids = []
    for e in event_ids:
        if e["telegram_id"] != telegram_id:
            other_events_ids.append(e["telegram_id"])

    for event_id in other_events_ids:
        if not await db_commands.check_returned_event_id(
                telegram_id=telegram_id, id_of_events_seen=event_id
        ):
            await db_commands.add_returned_event_id(
                telegram_id=telegram_id, id_of_events_seen=event_id
            )
            return event_id

    raise ValueError("No more event ids")


async def get_next_registration(telegram_id: int) -> List[int]:
    user = await db_commands.select_user(telegram_id=telegram_id)
    events: list = user.get("events")
    return events
