from aiogram.dispatcher.filters.state import State, StatesGroup


class Contacts(StatesGroup):
    select = State()
    search = State()
