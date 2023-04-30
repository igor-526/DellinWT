from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import datetime
import db_api
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import schedule_keys, day_keys, menu_keys, cancel_keys, confirm_keys
from funcs import convert_time, totaltime, converttimedelta, log


class Addtime(StatesGroup):
    s_time = State()
    f_time = State()
    day_status = State()
    confirm = State()
    change_date = State()


async def reg_s_time(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    res = convert_time(datetime.date.today(), message.text)
    if res:
        async with state.proxy() as data:
            data['start'] = res
        await message.answer("Во сколько по путевому листу вы закончили работать?", reply_markup=cancel_keys)
        await Addtime.f_time.set()
    else:
        await message.answer("Я вас не понял :(\nВведите время в формате ЧЧ.ММ, ЧЧ:ММ или ЧЧ ММ",
                             reply_markup=cancel_keys)


async def reg_f_time(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
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


async def reg_day_status(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
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


async def confirm(message: types.Message, state: FSMContext):
    if message.text == "Добавить запись":
        async with state.proxy() as data:
            await db_api.add_time(int(message.from_user.id),
                                      data['start'],
                                      data['end'],
                                      float(data["ttl"]["c"]),
                                      data["ttl"]['totalfloat'])
        await message.answer("Запись добавлена\n"
                                 "Выберите действие:", reply_markup=menu_keys)
        await log(message.from_user.id, "Added worktime to DB", str(data))
        await state.finish()
    elif message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    elif message.text == "Изменить дату":
        await Addtime.change_date.set()
        await message.answer("Пожалуйста, введите дату в формате ДД.ММ", reply_markup=cancel_keys)

async def ch_day(message: types.Message, state: FSMContext):
    if str(message.text) == "Отмена":
        await Addtime.confirm.set()
        await message.answer("Выберите действие:", reply_markup=confirm_keys)
        return
    try:
        async with state.proxy() as data:
            new_date = message.text.split(".")
            data['start'] = data['start'].replace(month = int(new_date[1]), day = int(new_date[0]))
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

def register_handlers_add_time(dp: Dispatcher):
    dp.register_message_handler(reg_s_time, state=Addtime.s_time)
    dp.register_message_handler(reg_f_time, state=Addtime.f_time)
    dp.register_message_handler(reg_day_status, state=Addtime.day_status)
    dp.register_message_handler(confirm, state=Addtime.confirm)
    dp.register_message_handler(ch_day, state=Addtime.change_date)
