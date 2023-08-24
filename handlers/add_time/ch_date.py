from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, confirm_keys
from funcs import log, converttimedelta
from handlers.add_time.fsmclass import Addtime
from handlers.commands.fsmclass import Menu


async def ch_date(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            new_date = message.text.split(".")
            data['start'] = data['start'].replace(month=int(new_date[1]), day=int(new_date[0]))
            data['end'] = data['end'].replace(month=int(new_date[1]), day=int(new_date[0]))
            await message.answer(f'Дата: {data["start"].strftime("%d.%m")}\n\n'
                                 f'Вы начали работать в {data["start"].strftime("%H:%M")}\n'
                                 f'Вы закончили работать в {data["end"].strftime("%H:%M")}\n'
                                 f'Ваш обед составляет: {converttimedelta(data["ttl"]["dinner"])}\n'
                                 f'В запись идёт следующее время: '
                                 f'{data["ttl"]["totalfloat"]:.2f} ч.\n\n'
                                 f'Хотите ли добавить эту запись?', reply_markup=confirm_keys)
            await log(message.from_user.id, "Calculated worktime", str(data))
            await Addtime.confirm.set()
    except:
        await message.answer("Я вас не понимаю :(\nПожалуйста, введите дату в формате ДД.ММ")


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


def register_handlers_at_ch_date(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Addtime.change_date, regexp='Отмена')
    dp.register_message_handler(ch_date, state=Addtime.change_date)
