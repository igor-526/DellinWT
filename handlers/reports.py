from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import db_api
from keyboards import menu_keys, reported_keys, cancel_keys, del_confirm_keys
from funcs import report_time, log, report_fuel, report_time_fordel
from datetime import date


class Reports(StatesGroup):
    select = State()
    time_reported = State()
    time_selectmonth = State()
    time_del = State()
    time_del_confirm = State()


async def select(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    if message.text == "Рабочее время":
        msg = await report_time.generate_msg(int(message.from_user.id), date.today().month)
        await log(message.from_user.id, "Report WorkTime", f'{str(date.today().month)}')
        await message.answer(msg, reply_markup=reported_keys)
        await Reports.time_reported.set()
    elif message.text == "Поездки":
        msg = await report_fuel.generate_msg(int(message.from_user.id), date.today().month)
        await message.answer(msg)


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


def register_handlers_reports(dp: Dispatcher):
    dp.register_message_handler(select, state=Reports.select)
    dp.register_message_handler(reported_t, state=Reports.time_reported)
    dp.register_message_handler(time_selmonth, state=Reports.time_selectmonth)
    dp.register_message_handler(time_del_sm, state=Reports.time_del)
    dp.register_message_handler(time_del_con, state=Reports.time_del_confirm)
