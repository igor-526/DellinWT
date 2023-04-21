from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import db_api
import funcs.report_fuel
from keyboards import menu_keys, reported_keys, cancel_keys, del_confirm_keys, report_keys
from funcs import report_time, log, report_fuel, report_time_fordel, gen_turnover, report_turnover_fordel
from datetime import date


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


async def select(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    elif message.text == "Рабочее время":
        msg = await report_time.generate_msg(int(message.from_user.id), date.today().month)
        await log(message.from_user.id, "Report WorkTime", f'{str(date.today().month)}')
        await message.answer(msg, reply_markup=reported_keys)
        await Reports.time_reported.set()
    elif message.text == "Поездки":
        msg = await report_fuel.calc(int(message.from_user.id), date.today().month)
        await message.answer(msg, reply_markup=reported_keys)
        await Reports.fuel_reported.set()
    elif message.text == "Оборот":
        msg = await gen_turnover(message.from_user.id, date.today().month)
        await message.answer(msg, reply_markup=reported_keys)
        await Reports.turnover_reported.set()
    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:", reply_markup=report_keys)


async def reported_t(message: types.Message, state: FSMContext):
    if message.text == "Меню":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    elif message.text == "Предыдущий месяц":
        msg = await report_time.generate_msg(int(message.from_user.id), date.today().month-1)
        await log(message.from_user.id, "Report WorkTime", f'{str(date.today().month-1)}')
        await message.answer(msg, reply_markup=reported_keys)
    elif message.text == "Другой месяц":
        await Reports.time_selectmonth.set()
        await message.answer("Введите номер месяца:", reply_markup=cancel_keys)
    elif message.text == "Удалить запись":
        await message.answer("За какую дату удалить записи? (ДД.ММ)", reply_markup=cancel_keys)
        await Reports.time_del.set()


async def time_selmonth(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    try:
        month = int(message.text)
        if 1 <= month <= 12:
            msg = await report_time.generate_msg(int(message.from_user.id), month)
            await log(message.from_user.id, "Report WorkTime", f'{str(month)}')
            await message.answer(msg, reply_markup=reported_keys)
            await Reports.time_reported.set()
        else:
            await message.answer("Я вас не понимаю :(\nВведите только число, соответствующее номеру месяца",
                                 reply_markup=cancel_keys)
    except:
        await message.answer("Я вас не понимаю :(\nВведите только число, соответствующее номеру месяца",
                             reply_markup=cancel_keys)


async def time_del_sm(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    try:
        async with state.proxy() as data:
            data['res'] = await report_time_fordel.calc(message.from_user.id, message.text)
            await message.answer(data["res"]["msg"], reply_markup=del_confirm_keys)
            await Reports.time_del_confirm.set()
    except:
        await message.answer("Я вас не понимаю :(\nПожалуйста, введите дату в формате ДД.ММ", reply_markup=cancel_keys)


async def time_del_con(message: types.Message, state: FSMContext):
    if message.text == "Меню":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    elif message.text == "Удалить записи":
        async with state.proxy() as data:
            await db_api.del_time(data["res"]["ids"])
        await message.answer("Записи успешно удалены", reply_markup=reported_keys)
        await Reports.time_reported.set()
    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка",
                             reply_markup=del_confirm_keys)


async def reported_tu(message: types.Message, state: FSMContext):
    if message.text == "Меню":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    elif message.text == "Предыдущий месяц":
        msg = await gen_turnover(message.from_user.id, date.today().month-1)
        await message.answer(msg, reply_markup=reported_keys)
    elif message.text == "Другой месяц":
        await Reports.turnover_selectmonth.set()
        await message.answer("Введите номер месяца:", reply_markup=cancel_keys)
    elif message.text == "Удалить запись":
        await message.answer("За какую дату удалить записи? (ДД.ММ)", reply_markup=cancel_keys)
        await Reports.turnover_del.set()


async def tu_selmonth(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    try:
        month = int(message.text)
        if 1 <= month <= 12:
            msg = await gen_turnover(message.from_user.id, month)
            await log(message.from_user.id, "Report WorkTime", f'{str(month)}')
            await message.answer(msg, reply_markup=reported_keys)
            await Reports.turnover_reported.set()
        else:
            raise
    except:
        await message.answer("Я вас не понимаю :(\nВведите только число, соответствующее номеру месяца",
                             reply_markup=cancel_keys)


async def tu_del_sm(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    try:
        async with state.proxy() as data:
            data['res'] = await report_turnover_fordel.calc(message.from_user.id, message.text)
            await message.answer(data["res"]["msg"], reply_markup=del_confirm_keys)
            await Reports.turnover_del_confirm.set()
    except:
        await message.answer("Я вас не понимаю :(\nПожалуйста, введите дату в формате ДД.ММ", reply_markup=cancel_keys)


async def tu_del_con(message: types.Message, state: FSMContext):
    if message.text == "Меню":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    elif message.text == "Удалить записи":
        async with state.proxy() as data:
            await db_api.del_turnover(data["res"]["ids"])
        await message.answer("Записи успешно удалены", reply_markup=reported_keys)
        await state.finish()
        await Reports.turnover_reported.set()
    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка",
                             reply_markup=del_confirm_keys)


async def reported_f(message: types.Message, state: FSMContext):
    if message.text == "Меню":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    elif message.text == "Предыдущий месяц":
        msg = await funcs.report_fuel.calc(message.from_user.id, date.today().month-1)
        await message.answer(msg, reply_markup=reported_keys)
    elif message.text == "Другой месяц":
        await Reports.fuel_selectmonth.set()
        await message.answer("Введите номер месяца:", reply_markup=cancel_keys)
    elif message.text == "Удалить запись":
        await message.answer("За какую дату удалить записи? (ДД.ММ)", reply_markup=cancel_keys)
        await Reports.fuel_del.set()


async def f_selmonth(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
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


async def f_del_sm(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    try:
        async with state.proxy() as data:
            data['res'] = await funcs.report_fuel.fordel(message.from_user.id, message.text)
            await message.answer(data["res"]["msg"], reply_markup=del_confirm_keys)
            await Reports.fuel_del_confirm.set()
    except:
        await message.answer("Я вас не понимаю :(\nПожалуйста, введите дату в формате ДД.ММ", reply_markup=cancel_keys)


async def f_del_con(message: types.Message, state: FSMContext):
    if message.text == "Меню":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    elif message.text == "Удалить записи":
        async with state.proxy() as data:
            await db_api.del_fuel(data["res"]["ids"])
        await message.answer("Записи успешно удалены", reply_markup=reported_keys)
        await state.finish()
        await Reports.fuel_reported.set()
    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка",
                             reply_markup=del_confirm_keys)


def register_handlers_reports(dp: Dispatcher):
    dp.register_message_handler(select, state=Reports.select)
    dp.register_message_handler(reported_t, state=Reports.time_reported)
    dp.register_message_handler(time_selmonth, state=Reports.time_selectmonth)
    dp.register_message_handler(time_del_sm, state=Reports.time_del)
    dp.register_message_handler(time_del_con, state=Reports.time_del_confirm)
    dp.register_message_handler(reported_tu, state=Reports.turnover_reported)
    dp.register_message_handler(tu_selmonth, state=Reports.turnover_selectmonth)
    dp.register_message_handler(tu_del_sm, state=Reports.turnover_del)
    dp.register_message_handler(tu_del_con, state=Reports.turnover_del_confirm)
    dp.register_message_handler(reported_f, state=Reports.fuel_reported)
    dp.register_message_handler(f_selmonth, state=Reports.fuel_selectmonth)
    dp.register_message_handler(f_del_sm, state=Reports.fuel_del)
    dp.register_message_handler(f_del_con, state=Reports.fuel_del_confirm)
