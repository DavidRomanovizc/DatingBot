import random

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from functions.event.extra_features import get_next_event, create_form, check_event_date, add_events_to_user
from functions.main_app.get_data_func import get_data_meetings
from keyboards.inline.poster_inline import poster_keyboard
from loader import dp, _


@dp.callback_query_handler(text="view_poster")
async def view_poster_handler(call: CallbackQuery, state: FSMContext):
    try:
        telegram_id = call.from_user.id
        event_list = await get_next_event(telegram_id)
        random_event = random.choice(event_list)
        await check_event_date(random_event)
        await create_form(form_owner=random_event, chat_id=telegram_id, call=call)
        await state.set_state("finding_event")
    except IndexError:
        await call.answer(_("На данный момент у нас нет подходящих мероприятий для вас"), show_alert=True)


@dp.callback_query_handler(lambda call: call.data.split('_')[0] == 'answer', state="finding_event")
async def list_poster_reaction(call: CallbackQuery, state: FSMContext):
    user = await get_data_meetings(call.from_user.id)
    is_admin = user[10]
    is_verification = user[6]
    call_data = call.data.split("-")

    if call_data[0] == "answer_notinteresting":
        await view_poster_handler(call, state)
    elif call_data[0] == "answer_imgoing":
        await add_events_to_user(call, event_id=int(call_data[1]))
        await view_poster_handler(call, state)
    elif call_data[0] == "answer_stopped_view":
        markup = await poster_keyboard(is_admin, is_verification)
        await call.message.delete()
        text = _("Рад был помочь, {fullname}!\n"
                 "Надеюсь, ты нашел кого-то благодаря мне").format(fullname=call.from_user.full_name)
        await call.message.answer(text, reply_markup=markup)
        await state.reset_state(with_data=False)
