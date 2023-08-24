from aiogram.dispatcher.filters.state import State, StatesGroup


class Settings(StatesGroup):
    sets = State()
    set_name = State()
    set_city = State()
    set_base = State()
    set_days = State()
    set_mode = State()
    del_profile = State()