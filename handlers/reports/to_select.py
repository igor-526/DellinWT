from aiogram import types, Dispatcher
from keyboards import menu_keys, reported_keys, cancel_keys, del_confirm_keys
from funcs import log, report_turnover_fordel, gen_turnover
from handlers.commands.fsmclass import Menu
from handlers.reports.fsmclass import Reports
from aiogram.dispatcher import FSMContext


async def menu(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


async def to_selmonth(message: types.Message):
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


async def to_del_sm(message: types.Message, state: FSMContext):
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


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:", reply_markup=cancel_keys)


def register_handlers_reports_to_select(dp: Dispatcher):
    dp.register_message_handler(menu, state=Reports.turnover_selectmonth, regexp="Отмена")
    dp.register_message_handler(menu, state=Reports.turnover_del, regexp="Отмена")
    dp.register_message_handler(to_selmonth, state=Reports.turnover_selectmonth)
    dp.register_message_handler(to_del_sm, state=Reports.turnover_del)
    dp.register_message_handler(inval, state=Reports.turnover_selectmonth)
    dp.register_message_handler(inval, state=Reports.turnover_del)
