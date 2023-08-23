from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, cancel_keys
from handlers.calc_fuel.fsmclass import Calculate


async def s_odo(message: types.Message, state: FSMContext):
    try:
        val = int(message.text)
        if val >= 0:
            async with state.proxy() as data:
                data['start_odo'] = val
            await Calculate.f_odometer.set()
            await message.answer("Отлично! Теперь введите конечный пробег:", reply_markup=cancel_keys)
        else:
            await message.answer("Пробег не может быть отрицательным\n"
                                 "Попробуйте ещё раз!", reply_markup=cancel_keys)
    except:
        await message.answer("Я так не понимаю :(\n"
                             "Напишите мне сообщение, содержащее исключительно число, соответствующее "
                             "начальному пробегу транспортного средства при открытии путевого листа",
                             reply_markup=cancel_keys)


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Выберите действие:", reply_markup=menu_keys)


def register_handlers_cf_s_odo(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Calculate.s_odometer, regexp='Отмена')
    dp.register_message_handler(s_odo, state=Calculate.s_odometer)
