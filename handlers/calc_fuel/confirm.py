from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys
from handlers.calc_fuel.fsmclass import Calculate
from handlers.commands.fsmclass import Menu
from funcs import log
import db_api
from datetime import date


async def add_note(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await db_api.add_fuel(driver=message.from_id,
                              milleage=data['result']['odo'],
                              fuel_delta=data['result']['fuel_delta'],
                              s_odo=data['start_odo'],
                              f_odo=data['finish_odo'],
                              s_fuel=data['fuel'],
                              f_fuel=data['result']['fuel'],
                              auto=data['result']['auto_id'],
                              date=date.today())
    await message.answer("Запись добавлена\n"
                         "Выберите действие:", reply_markup=menu_keys)
    await log(message.from_user.id, "Added fuel to DB", f'{data["result"]}')
    await Menu.menu.set()


async def cancel(message: types.Message):
    await Menu.menu.set()
    await message.answer("Выберите действие:", reply_markup=menu_keys)


def register_handlers_cf_confirm(dp: Dispatcher):
    dp.register_message_handler(add_note, state=Calculate.confirm, regexp="Добавить запись")
    dp.register_message_handler(cancel, state=Calculate.confirm, regexp='Отмена')
