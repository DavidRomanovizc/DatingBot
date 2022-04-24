from aiogram.dispatcher.filters.state import State, StatesGroup


class BanUser(StatesGroup):
    ban = State()
    unban = State()

    ask_id = State()

    ban_complete = State()
    unban_complete = State()
