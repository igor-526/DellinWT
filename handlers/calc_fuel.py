from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import auto_keys
from funcs import calc_fuel
from keyboards import menu_keys

class Calculate(StatesGroup):
    s_odometer = State()
    f_odometer = State()
    fuel = State()
    refuel = State()
    sel_auto = State()


async def ask_f_odo(message: types.Message, state: FSMContext):
    try:
        val = int(message.text)
        if val >= 0:
            async with state.proxy() as data:
                data['start_odo'] = val
            await Calculate.f_odometer.set()
            await message.answer("Отлично! Теперь введите конечный пробег:")
        else:
            await message.answer("Пробег не может быть отрицательным\n"
                                 "Попробуйте ещё раз!")
    except:
        await message.answer("Я так не понимаю :(\n"
                             "Напишите мне сообщение, содержащее исключительно число, соответствующее начальному пробегу "
                             "транспортного средства при открытии путевого листа")


async def ask_fuel(message: types.Message, state: FSMContext):
    try:
        val = int(message.text)
        async with state.proxy() as data:
            if val > data['start_odo']:
                data['finish_odo'] = val
                await Calculate.fuel.set()
                await message.answer("Отлично! Теперь введите остаток в баке в начале дня:")
            else:
                await message.answer("Пробег не может быть меньшим или равным пробегу при открытии путевого листа\n"
                                     "Попробуйте ещё раз!")
    except:
        await message.answer("Я так не понимаю :(\n"
                             "Напишите мне сообщение, содержащее исключительно число, соответствующее конечному пробегу "
                             "транспортного средства при закрытии путевого листа")


async def ask_refuel(message: types.Message, state: FSMContext):
    try:
        val = float(message.text)
        if val >= 1:
            async with state.proxy() as data:
                data['fuel'] = val
            await Calculate.refuel.set()
            await message.answer("Подскажите, вы заправлялись? Введите количество заправленных литров:\n"
                                 "Если не заправлялись, введите 0")
        else:
            await message.answer("Остаток топлива не может быть меньше 1\n"
                                 "Пожалуйста, введите значение, соответствующее значению остатка топлива при "
                                 "открытии путевого листа")
    except:
        await message.answer("Я так не понимаю :(\n"
                             "Напишите мне сообщение, содержащее исключительно число, соответствующее значению остатка "
                             "топлива транспортного средства при открытии путевого листа")


async def ask_auto(message: types.Message, state: FSMContext):
    try:
        val = float(message.text)
        if val >= 0:
            async with state.proxy() as data:
                data['refuel'] = val
            await Calculate.sel_auto.set()
            await message.answer("Отлично! Последнее - выберите ТС:", reply_markup=await auto_keys())
        else:
            await message.answer("Количество заправленного топлива не может быть отрицательным\n"
                                 "Попробуйте ещё раз")
    except:
            await message.answer("Я так не понимаю :(\n"
                             "Напишите мне сообщение, содержащее исключительно число, соответствующее значению выданного "
                             "топлива транспортного средства при закрытии путевого листа")


async def calc_result(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['auto'] = str(message.text)
            result = await calc_fuel(dict(data))
            await message.answer(f'Ваш автомобиль: {result["auto"]}\n'
                                 f'Его расход: {result["consumption"]}\n'
                                 f'Его ёмкость бака: {result["tank"]}\n\n'
                                 f'Вы проехали: {result["odo"]}\n'
                                 f'Остаток топлива: {result["fuel"]}',
                                 reply_markup=menu_keys)
        await state.finish()
    except:
        await message.answer("Я так не понимаю :(\n"
                             "Выберите автомобиль из списка:", reply_markup=await auto_keys())

def register_handlers_calc_fuel(dp: Dispatcher):
    dp.register_message_handler(ask_f_odo, state=Calculate.s_odometer)
    dp.register_message_handler(ask_fuel, state=Calculate.f_odometer)
    dp.register_message_handler(ask_refuel, state=Calculate.fuel)
    dp.register_message_handler(ask_auto, state=Calculate.refuel)
    dp.register_message_handler(calc_result, state=Calculate.sel_auto)