from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, schedule_keys
from handlers.turnover.fsmclass import Turnover
from handlers.commands.fsmclass import Menu
import db_api
from datetime import date


async def add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await db_api.add_turnover(message.from_user.id, data['turnover'], date.today())
    await Menu.menu.set()
    await message.answer("Оборот успешно добавлен!\nВыберите действие:", reply_markup=menu_keys)


async def cancel(message: types.Message):
    await Menu.menu.set()
    await message.answer("Выберите действие:", reply_markup=menu_keys)


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:",
                         reply_markup=schedule_keys)


def register_handlers_turnover_confirm(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Turnover.confirm, regexp="Нет")
    dp.register_message_handler(add, state=Turnover.confirm, regexp="Да")
    dp.register_message_handler(inval, state=Turnover.confirm)
