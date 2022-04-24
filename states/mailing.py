from aiogram.dispatcher.filters.state import StatesGroup, State


class Mailing(StatesGroup):
    stage1 = State()
    stage2 = State()
    stage3 = State()
