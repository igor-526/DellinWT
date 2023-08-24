from aiogram.dispatcher.filters.state import State, StatesGroup


class Reports(StatesGroup):
    select = State()
    time_reported = State()
    time_selectmonth = State()
    time_del = State()
    time_del_confirm = State()
    turnover_reported = State()
    turnover_selectmonth = State()
    turnover_del = State()
    turnover_del_confirm = State()
    fuel_reported = State()
    fuel_selectmonth = State()
    fuel_del = State()
    fuel_del_confirm = State()
