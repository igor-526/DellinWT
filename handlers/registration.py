from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import db_api
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import city_keys, base_keys, schedule_keys, menu_keys
from funcs import get_wdays
from datetime import date


class Registration(StatesGroup):
    city = State()
    base = State()
    schedule = State()
    days = State()
    instruction = State()


async def city(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['city'] = int(await db_api.city_id(message.text))
            await message.answer("Отлично! С городом определились\nТеперь выберите ваш ОСП",
                                    reply_markup=await base_keys(data['city']))
            await Registration.base.set()
    except:
        await message.answer("К сожалению, данный город ещё не поддерживается :(\nПожалуйста, выберите из списка",
                       reply_markup=await city_keys())


async def base(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['base'] = int(await db_api.base_id(message.text))
            await message.answer("Отлично! С базой определились!\nПодскажите, вы работаете в графике 5/2?",
                                 reply_markup=schedule_keys)
            await Registration.schedule.set()
    except:
        async with state.proxy() as data:
            await message.answer("К сожалению, данное ОСП ещё не поддерживается :(\nПожалуйста, выберите из списка",
                                 reply_markup=await base_keys(data['city']))


async def schedule(message: types.Message, state: FSMContext):
    if message.text == "Да":
        async with state.proxy() as data:
            data['mode'] = 1
            data['wdays'] = get_wdays(date.today().month, date.today().year)
        await message.answer(f"В этом месяце у вас {data['wdays']['work']} рабочих дней\n"
                             f"Это {data['wdays']['hours']} часов!\n"
                             f"Далее бот будет рассчитывать по этому количеству, а каждый месяц обновлять норму\n"
                             f"Поменять это поведение можно будет в настройках")
        await message.answer("Хотите ли вы прочитать инструкцию по работе с ботом?", reply_markup=schedule_keys)
        await Registration.instruction.set()

    elif message.text == "Нет":
        async with state.proxy() as data:
            data['mode'] = 2
        await message.answer("Введите количество рабочих дней в этом месяце:\n"
                             "Далее это можно будет поменять в настройках")
        await Registration.days.set()

    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите вариант.\nВы работаете в графике 5/2?",
                             reply_markup=schedule_keys)


async def work_days(message: types.Message, state: FSMContext):
    try:
        days = int(message.text)
        if 1 <= days <= 31:
            hours = days * 8
            async with state.proxy() as data:
                data['wdays'] = {'work': days, 'hours': hours}
                await message.answer(f"В этом месяце у вас {data['wdays']['work']} рабочих дней\n"
                                     f"Это {data['wdays']['hours']} часов!\n"
                                     f"Далее бот будет рассчитывать по этому количеству, а каждый месяц предлагать "
                                     f"обновлять норму\n"
                                     f"Поменять это поведение можно будет в настройках")
                await Registration.instruction.set()
                await message.answer("Хотите ли вы прочитать инструкцию по работе с ботом?", reply_markup=schedule_keys)
        else:
            await message.answer("Я вас не понимаю :(\nПожалуйста, введите количество рабочих дней по плану вашего "
                           "производственного календаря")
    except:
        await message.answer("Я вас не понимаю :(\nПожалуйста, введите количество рабочих дней по плану вашего "
                             "производственного календаря")


async def instruct(message: types.Message, state: FSMContext):
    if message.text == "Нет":
        async with state.proxy() as data:
            await db_api.add_user(message.from_user.id, message.from_user.first_name,
                                  data['city'], data['base'], data['mode'], data['wdays']['work'])
        await message.answer("Вы успешно зарегистрировались!\nВыберите действие:", reply_markup=menu_keys)
        await state.finish()
    elif message.text == "Да":
        async with state.proxy() as data:
            await db_api.add_user(message.from_user.id, message.from_user.first_name,
                                  data['city'], data['base'], data['mode'], data['wdays']['work'])
        await message.answer("А инструкция пока не написана((")
        await message.answer("Вы успешно зарегистрировались!\nВыберите действие:", reply_markup=menu_keys)
        await state.finish()
    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите из списка")


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(city, state=Registration.city)
    dp.register_message_handler(base, state=Registration.base)
    dp.register_message_handler(schedule, state=Registration.schedule)
    dp.register_message_handler(work_days, state=Registration.days)
    dp.register_message_handler(instruct, state=Registration.instruction)