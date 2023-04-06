from pprint import pprint
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import datetime
import db_api
from create_bot import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import schedule_keys
from keyboards import day_keys
from keyboards import menu_keys


class Addtime(StatesGroup):
    reg = State()
    s_time = State()
    f_time = State()
    day_status = State()


def converttime(date, time):
    try:
        n_time = time.split(".")
        res = datetime.datetime(date.year, date.month, date.day, int(n_time[0]), int(n_time[1]), 0, 0)
        return res
    except:
        return False

def totaltime(start, end, c):
    ttl = {}
    ttl['time'] = end - start
    ttl['dinner'] = datetime.timedelta(hours=1)
    ttl['total'] = (ttl['time'] - ttl['dinner']) * c
    ttl['totalfloat'] = float(ttl['total'].seconds/3600)
    return ttl


async def reg_schedule(message: types.Message, state: FSMContext):
    if message.text == "5/2":
        await message.answer("Ваша рабочая норма: 160 часов в неделю!")
        await db_api.add_wt(int(message.from_user.id), 160)
        await message.answer("Во сколько по путевому листу вы начали работать?\n"
                             "ЧЧ.MM")
        await Addtime.s_time.set()
    elif message.text == "2/2":
        await message.answer("Ваша рабочая норма: 136 часов в неделю!")
        await db_api.add_wt(int(message.from_user.id), 136)
        await message.answer("Во сколько по путевому листу вы начали работать?\n"
                             "ЧЧ.MM")
        await Addtime.s_time.set()
    else:
        await message.answer("Я так не понимаю :(\n"
                             "Пожалуйста, выберите один из графиков:", reply_markup=schedule_keys)


async def reg_s_time(message: types.Message, state: FSMContext):
    res = converttime(datetime.date.today(), message.text)
    if res:
        async with state.proxy() as data:
            data['start'] = res
        await message.answer("Во сколько по путевому листу вы закончили работать?\n"
                                 "ЧЧ.MM")
        await Addtime.f_time.set()
    else:
        await message.answer("Я вас не понял :(\nВведите время в формате ЧЧ.ММ")


async def reg_f_time(message: types.Message, state: FSMContext):
    res = converttime(datetime.date.today(), message.text)
    if res:
        async with state.proxy() as data:
            if res > data['start']:
                data['end'] = res
                await message.answer("Как зарегистрировать данный рабочий день?", reply_markup=day_keys)
                await Addtime.day_status.set()
            else:
                await message.answer('Ошибка! Время завершения рабочего дня меньше времени начала рабочего дня!\n'
                                     'Если вы закончили работать в других сутках, укажите "23.59", после чего добавьте '
                                     'новый рабочий день')
    else:
        await message.answer("Я вас не понял :(\nВведите время в формате ЧЧ.ММ")


async def reg_day_status(message: types.Message, state: FSMContext):
    c = None
    if message.text == "Обычный день":
        c = 1
    elif message.text == "Выход в выходной":
        c = 2
    elif message.text == "Выход в праздничный":
        c = 2
    else:
        await message.answer("Я так не понимаю :(\n"
                             "Пожалуйста, выберите вариант:", reply_markup=day_keys)
    if c:
        async with state.proxy() as data:
            ttl = totaltime(data['start'], data['end'], c)
            await db_api.add_time(int(message.from_user.id),
                            data['start'],
                            data['end'],
                            float(c),
                            ttl['totalfloat'])
            await message.answer(f'Вы начали работать в {data["start"].hour}:{data["start"].minute}\n'
                                 f'Вы закончили работать в {data["end"].hour}:{data["end"].minute}\n'
                                 f'Ваш обед составляет: 01:00\n'
                                 f'В запись идёт следующее время: {ttl["total"]}')
            await message.answer("Выберите действие:", reply_markup=menu_keys)
            await state.finish()


def register_handlers_add_time(dp: Dispatcher):
    dp.register_message_handler(reg_schedule, state=Addtime.reg)
    dp.register_message_handler(reg_s_time, state=Addtime.s_time)
    dp.register_message_handler(reg_f_time, state=Addtime.f_time)
    dp.register_message_handler(reg_day_status, state=Addtime.day_status)