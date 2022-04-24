from aiogram.dispatcher.filters.state import State, StatesGroup


class FindUser(StatesGroup):
    start_find = State()
    process_find1 = State()
    finish_find = State()
