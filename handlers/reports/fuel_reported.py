from aiogram import types, Dispatcher
from keyboards import menu_keys, reported_keys, report_keys, cancel_keys
import funcs.report_fuel
from datetime import date
from handlers.commands.fsmclass import Menu
from handlers.reports.fsmclass import Reports


async def menu(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


async def prev_m(message: types.Message):
    msg = await funcs.report_fuel.calc(message.from_user.id, date.today().month - 1)
    await message.answer(msg, reply_markup=reported_keys)


async def another_m(message: types.Message):
    await Reports.fuel_selectmonth.set()
    await message.answer("Введите номер месяца:", reply_markup=cancel_keys)


async def delete(message: types.Message):
    await message.answer("За какую дату удалить записи? (ДД.ММ)", reply_markup=cancel_keys)
    await Reports.fuel_del.set()


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:", reply_markup=report_keys)


def register_handlers_reports_fuel(dp: Dispatcher):
    dp.register_message_handler(menu, state=Reports.fuel_reported, regexp="Меню")
    dp.register_message_handler(prev_m, state=Reports.fuel_reported, regexp="Предыдущий месяц")
    dp.register_message_handler(another_m, state=Reports.fuel_reported, regexp="Другой месяц")
    dp.register_message_handler(delete, state=Reports.fuel_reported, regexp="Удалить запись")
    dp.register_message_handler(inval, state=Reports.fuel_reported)
