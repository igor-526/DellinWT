from aiogram.dispatcher.filters.state import State, StatesGroup


class Addtime(StatesGroup):
    s_time = State()
    f_time = State()
    day_status = State()
    confirm = State()
    change_date = State()