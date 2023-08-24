from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, auto_keys, cancel_keys
from handlers.calc_fuel.fsmclass import Calculate
from handlers.commands.fsmclass import Menu


async def no_refuel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['refuel'] = 0
    await Calculate.sel_auto.set()
    await message.answer("Отлично! Последнее - выберите ТС:", reply_markup=await auto_keys())


async def refuel(message: types.Message, state: FSMContext):
    try:
        val = float(message.text)
        if val >= 0:
            async with state.proxy() as data:
                data['refuel'] = val
            await Calculate.sel_auto.set()
            await message.answer("Отлично! Последнее - выберите ТС:", reply_markup=await auto_keys())
        else:
            await message.answer("Количество заправленного топлива не может быть отрицательным\n"
                                 "Попробуйте ещё раз", reply_markup=cancel_keys)
    except:
        await message.answer("Я так не понимаю :(\n"
                             "Напишите мне сообщение, содержащее исключительно число, соответствующее значению"
                             "выданного топлива транспортного средства при закрытии путевого листа",
                             reply_markup=cancel_keys)


async def cancel(message: types.Message):
    await Menu.menu.set()
    await message.answer("Выберите действие:", reply_markup=menu_keys)


def register_handlers_cf_refuel(dp: Dispatcher):
    dp.register_message_handler(no_refuel, state=Calculate.refuel, regexp='Нет')
    dp.register_message_handler(cancel, state=Calculate.refuel, regexp='Отмена')
    dp.register_message_handler(refuel, state=Calculate.refuel)
