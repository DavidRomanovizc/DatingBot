from aiogram.dispatcher.filters.state import State, StatesGroup


class ViewStates(StatesGroup):
    id_ = State()
    message = State()
