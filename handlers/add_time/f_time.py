from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import datetime
from keyboards import menu_keys, cancel_keys, day_keys
from funcs import convert_time
from handlers.add_time.fsmclass import Addtime
from handlers.commands.fsmclass import Menu


async def reg_f_time(message: types.Message, state: FSMContext):
    res = convert_time(datetime.date.today(), message.text)
    if res:
        async with state.proxy() as data:
            if res > data['start']:
                data['end'] = res
                await message.answer("Как зарегистрировать данный рабочий день?", reply_markup=day_keys)
                await Addtime.day_status.set()
            else:
                await message.answer('Ошибка! Время завершения рабочего дня меньше времени начала рабочего дня!\n'
                                     'Если вы закончили работать в других сутках, укажите "23.59", после чего добавьте '
                                     'новый рабочий день', reply_markup=cancel_keys)
    else:
        await message.answer("Я вас не понял :(\nВведите время в формате ЧЧ.ММ, ЧЧ:ММ или ЧЧ ММ",
                             reply_markup=cancel_keys)


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


def register_handlers_at_f_time(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Addtime.f_time, regexp='Отмена')
    dp.register_message_handler(reg_f_time, state=Addtime.f_time)
