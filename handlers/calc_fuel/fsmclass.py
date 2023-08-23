from aiogram.dispatcher.filters.state import State, StatesGroup

class Calculate(StatesGroup):
    s_odometer = State()
    f_odometer = State()
    fuel = State()
    ask_refuel = State()
    refuel = State()
    sel_auto = State()
    confirm = State()