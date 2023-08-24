from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    city = State()
    base = State()
    schedule = State()
    days = State()
    instruction = State()
