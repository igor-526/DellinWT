from pprint import pprint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import datetime
import db_api
from create_bot import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import schedule_keys
from keyboards import day_keys


class Addtime(StatesGroup):
    reg = State()
    s_time = State()
    f_time = State()
    day_status = State()


def converttime(time):
    dt = (datetime.datetime.strptime("01.00", "%H.%M"))
    return dt

def totaltime(start, end, c):
    delta = end - start
    ttl = delta * 2
    total = {}
    total['worked'] = delta
    total['total'] = ttl
    pprint(total)
    print(str(total['worked']))
    return total



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
    async with state.proxy() as data:
        data['date'] = datetime.date.today()
        data['start'] = converttime(message.text)
    await message.answer("Во сколько по путевому листу вы закончили работать?\n"
                         "ЧЧ.MM")
    await Addtime.f_time.set()


async def reg_f_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['end'] = converttime(message.text)
    await message.answer("Как зарегистрировать данный рабочий день?", reply_markup=day_keys)
    await Addtime.day_status.set()


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
            await db_api.add_time(int(message.from_user.id),
                            data['date'],
                            data['start'],
                            data['end'],
                            float(c))
            totaltime(data['start'], data['end'], 1)


def register_handlers_add_time(dp: Dispatcher):
    dp.register_message_handler(reg_schedule, state=Addtime.reg)
    dp.register_message_handler(reg_s_time, state=Addtime.s_time)
    dp.register_message_handler(reg_f_time, state=Addtime.f_time)
    dp.register_message_handler(reg_day_status, state=Addtime.day_status)