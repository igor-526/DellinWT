from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, day_keys, confirm_keys
from funcs import totaltime, converttimedelta, log
from handlers.add_time.fsmclass import Addtime
from handlers.commands.fsmclass import Menu


async def day_status(message: types.Message, state: FSMContext):
    c = None
    if message.text == "Обычный день":
        c = 1
    elif message.text == "Выход в выходной/праздничный":
        c = 2
    else:
        await message.answer("Я так не понимаю :(\n"
                             "Пожалуйста, выберите вариант:", reply_markup=day_keys)
    if c:
        async with state.proxy() as data:
            data["ttl"] = totaltime(data['start'], data['end'], c)
            await message.answer(f'Дата: {data["start"].strftime("%d.%m")}\n\n'
                                 f'Вы начали работать в {data["start"].strftime("%H:%M")}\n'
                                 f'Вы закончили работать в {data["end"].strftime("%H:%M")}\n'
                                 f'Ваш обед составляет: {converttimedelta(data["ttl"]["dinner"])}\n'
                                 f'В запись идёт следующее время: '
                                 f'{data["ttl"]["totalfloat"]:.2f} ч.\n\n'
                                 f'Хотите ли добавить эту запись?', reply_markup=confirm_keys)
            await log(message.from_user.id, "Calculated worktime", str(data))
            await Addtime.confirm.set()


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


def register_handlers_at_day_status(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Addtime.day_status, regexp='Отмена')
    dp.register_message_handler(day_status, state=Addtime.day_status)
