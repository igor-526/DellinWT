from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, cancel_keys, refuel_keys
from handlers.calc_fuel.fsmclass import Calculate
from handlers.commands.fsmclass import Menu


async def fuel(message: types.Message, state: FSMContext):
    try:
        val = float(message.text)
        if val >= 1:
            async with state.proxy() as data:
                data['fuel'] = val
            await Calculate.refuel.set()
            await message.answer("Подскажите, вы заправлялись?\n"
                                 "Если да, то введите количество заправленных литров", reply_markup=refuel_keys)
        else:
            await message.answer("Остаток топлива не может быть меньше 1\n"
                                 "Пожалуйста, введите значение, соответствующее значению остатка топлива при "
                                 "открытии путевого листа", reply_markup=cancel_keys)
    except:
        await message.answer("Я так не понимаю :(\n"
                             "Напишите мне сообщение, содержащее исключительно число, соответствующее значению остатка "
                             "топлива транспортного средства при открытии путевого листа", reply_markup=cancel_keys)


async def cancel(message: types.Message):
    await Menu.menu.set()
    await message.answer("Выберите действие:", reply_markup=menu_keys)


def register_handlers_cf_fuel(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Calculate.fuel, regexp='Отмена')
    dp.register_message_handler(fuel, state=Calculate.fuel)
