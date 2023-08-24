from aiogram import types, Dispatcher
from keyboards import menu_keys, reported_keys, cancel_keys, del_confirm_keys
from funcs import log
from handlers.commands.fsmclass import Menu
from handlers.reports.fsmclass import Reports
from aiogram.dispatcher import FSMContext
import funcs.report_fuel


async def menu(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


async def fuel_selmonth(message: types.Message):
    try:
        month = int(message.text)
        if 1 <= month <= 12:
            msg = await funcs.report_fuel.calc(message.from_user.id, month)
            await log(message.from_user.id, "Report Fuel", f'{str(month)}')
            await message.answer(msg, reply_markup=reported_keys)
            await Reports.fuel_reported.set()
        else:
            raise
    except:
        await message.answer("Я вас не понимаю :(\nВведите только число, соответствующее номеру месяца",
                             reply_markup=cancel_keys)


async def fuel_del_sm(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['res'] = await funcs.report_fuel.fordel(message.from_user.id, message.text)
            await message.answer(data["res"]["msg"], reply_markup=del_confirm_keys)
            await Reports.fuel_del_confirm.set()
    except:
        await message.answer("Я вас не понимаю :(\nПожалуйста, введите дату в формате ДД.ММ", reply_markup=cancel_keys)


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:", reply_markup=cancel_keys)


def register_handlers_reports_fuel_select(dp: Dispatcher):
    dp.register_message_handler(menu, state=Reports.fuel_selectmonth, regexp="Отмена")
    dp.register_message_handler(menu, state=Reports.fuel_del, regexp="Отмена")
    dp.register_message_handler(fuel_selmonth, state=Reports.fuel_selectmonth)
    dp.register_message_handler(fuel_del_sm, state=Reports.fuel_del)
    dp.register_message_handler(inval, state=Reports.fuel_selectmonth)
    dp.register_message_handler(inval, state=Reports.fuel_del)
