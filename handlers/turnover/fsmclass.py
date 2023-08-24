from aiogram.dispatcher.filters.state import State, StatesGroup


class Turnover(StatesGroup):
    add = State()
    confirm = State()
