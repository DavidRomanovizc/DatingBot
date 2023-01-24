import random

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from functions.event.extra_features import get_next_event, create_form
from loader import dp, _


@dp.callback_query_handler(text="my_appointment")
async def get_event_list(call: CallbackQuery, state: FSMContext):
    try:
        telegram_id = call.from_user.id
        event_list = await get_next_event(telegram_id)
        random_event = random.choice(event_list)
        await create_form(form_owner=random_event, chat_id=telegram_id, call=call, view=False)
        await state.set_state("cancel_record")
    except IndexError:
        await call.answer(_("На данный момент у нас нет подходящих мероприятий для вас"), show_alert=True)


@dp.callback_query_handler(lambda call: call.data.split('-')[0] == "cancel", state="cancel_record")
async def list_poster_reaction(call: CallbackQuery, state: FSMContext):
    call_data = call.data.split("-")

    if call_data[0] == 'cancel':
        await get_event_list(call, state)
