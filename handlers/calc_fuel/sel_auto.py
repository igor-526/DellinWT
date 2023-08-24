from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, confirm_keys, auto_keys
from handlers.calc_fuel.fsmclass import Calculate
from funcs import calc_fuel, log
from handlers.commands.fsmclass import Menu


async def sel_auto(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['auto'] = str(message.text)
            result = await calc_fuel(dict(data))
            data['result'] = result
            await message.answer(f'Ваш автомобиль: {result["auto"]}\n'
                                 f'Его расход: {result["consumption"]}\n'
                                 f'Его ёмкость бака: {result["tank"]}\n\n'
                                 f'Вы проехали: {result["odo"]}\n'
                                 f'Остаток топлива: {result["fuel"]}')
            await log(message.from_user.id, "Calculate fuel", str(result))
        await message.answer("Добавить запись?", reply_markup=confirm_keys)
        await Calculate.confirm.set()
    except:
        await message.answer("Я так не понимаю :(\n"
                             "Выберите автомобиль из списка:", reply_markup=await auto_keys())


async def cancel(message: types.Message, state: FSMContext):
    await Menu.menu.set()
    await message.answer("Выберите действие:", reply_markup=menu_keys)


def register_handlers_cf_sel_auto(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Calculate.sel_auto, regexp='Отмена')
    dp.register_message_handler(sel_auto, state=Calculate.sel_auto)
