from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, cancel_keys
from handlers.calc_fuel.fsmclass import Calculate
from handlers.commands.fsmclass import Menu


async def f_odo(message: types.Message, state: FSMContext):
    try:
        val = int(message.text)
        async with state.proxy() as data:
            if val > data['start_odo']:
                data['finish_odo'] = val
                await Calculate.fuel.set()
                await message.answer("Отлично! Теперь введите остаток в баке в начале дня:", reply_markup=cancel_keys)
            else:
                await message.answer("Пробег не может быть меньшим или равным пробегу при открытии путевого листа\n"
                                     "Попробуйте ещё раз!", reply_markup=cancel_keys)
    except:
        await message.answer("Я так не понимаю :(\n"
                             "Напишите мне сообщение, содержащее исключительно число, "
                             "соответствующее конечному пробегу транспортного средства при закрытии путевого листа",
                             reply_markup=cancel_keys)


async def cancel(message: types.Message):
    await Menu.menu.set()
    await message.answer("Выберите действие:", reply_markup=menu_keys)


def register_handlers_cf_f_odo(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Calculate.f_odometer, regexp='Отмена')
    dp.register_message_handler(f_odo, state=Calculate.f_odometer)
