from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import datetime
from keyboards import menu_keys, cancel_keys
from funcs import convert_time
from handlers.add_time.fsmclass import Addtime
from handlers.commands.fsmclass import Menu


async def reg_s_time(message: types.Message, state: FSMContext):
    res = convert_time(datetime.date.today(), message.text)
    if res:
        async with state.proxy() as data:
            data['start'] = res
        await message.answer("Во сколько по путевому листу вы закончили работать?", reply_markup=cancel_keys)
        await Addtime.f_time.set()
    else:
        await message.answer("Я вас не понял :(\nВведите время в формате ЧЧ.ММ, ЧЧ:ММ или ЧЧ ММ",
                             reply_markup=cancel_keys)


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


def register_handlers_at_s_time(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Addtime.s_time, regexp='Отмена')
    dp.register_message_handler(reg_s_time, state=Addtime.s_time)
