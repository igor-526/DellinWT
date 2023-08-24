from aiogram.dispatcher.filters.state import State, StatesGroup

class Menu(StatesGroup):
    menu = State()
    msgall = State()