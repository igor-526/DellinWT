from aiogram import types, Dispatcher
from keyboards import menu_keys, reported_keys, report_keys, cancel_keys, del_confirm_keys
from funcs import report_time, log, report_time_fordel
from handlers.commands.fsmclass import Menu
from handlers.reports.fsmclass import Reports
from aiogram.dispatcher import FSMContext


async def menu(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


async def time_selmonth(message: types.Message):
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
    try:
        async with state.proxy() as data:
            data['res'] = await report_time_fordel.calc(message.from_user.id, message.text)
            await message.answer(data["res"]["msg"], reply_markup=del_confirm_keys)
            await Reports.time_del_confirm.set()
    except:
        await message.answer("Я вас не понимаю :(\nПожалуйста, введите дату в формате ДД.ММ", reply_markup=cancel_keys)


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:", reply_markup=cancel_keys)


def register_handlers_reports_time_select(dp: Dispatcher):
    dp.register_message_handler(menu, state=Reports.time_selectmonth, regexp="Отмена")
    dp.register_message_handler(menu, state=Reports.time_del, regexp="Отмена")
    dp.register_message_handler(time_selmonth, state=Reports.time_selectmonth)
    dp.register_message_handler(time_del_sm, state=Reports.time_del)
    dp.register_message_handler(inval, state=Reports.time_selectmonth)
    dp.register_message_handler(inval, state=Reports.time_del)
