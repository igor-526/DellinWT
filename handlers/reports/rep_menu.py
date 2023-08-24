from aiogram import types, Dispatcher
from keyboards import menu_keys, reported_keys, report_keys
from funcs import report_time, log, report_fuel, gen_turnover
from datetime import date
from handlers.commands.fsmclass import Menu
from handlers.reports.fsmclass import Reports


async def worktime(message: types.Message):
    msg = await report_time.generate_msg(int(message.from_user.id), date.today().month)
    await log(message.from_user.id, "Report WorkTime", f'{str(date.today().month)}')
    await message.answer(msg, reply_markup=reported_keys)
    await Reports.time_reported.set()


async def fuel(message: types.Message):
    msg = await report_fuel.calc(int(message.from_user.id), date.today().month)
    await message.answer(msg, reply_markup=reported_keys)
    await Reports.fuel_reported.set()


async def turnover(message: types.Message):
    msg = await gen_turnover(message.from_user.id, date.today().month)
    await message.answer(msg, reply_markup=reported_keys)
    await Reports.turnover_reported.set()


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:", reply_markup=report_keys)


def register_handlers_reports_menu(dp: Dispatcher):
    dp.register_message_handler(worktime, state=Reports.select, regexp="Рабочее время")
    dp.register_message_handler(fuel, state=Reports.select, regexp="Поездки")
    dp.register_message_handler(turnover, state=Reports.select, regexp="Оборот")
    dp.register_message_handler(cancel, state=Reports.select, regexp="Отмена")
    dp.register_message_handler(inval, state=Reports.select)
