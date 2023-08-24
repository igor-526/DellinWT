from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from funcs import get_wdays
from keyboards import schedule_keys
from handlers.registration.fsmclass import Registration
from datetime import date


async def schedule_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mode'] = 1
        data['wdays'] = await get_wdays(date.today().month, date.today().year)
    await message.answer(f"В этом месяце у вас {data['wdays']['work']} рабочих дней\n"
                         f"Это {data['wdays']['hours']} часов!\n"
                         f"Далее бот будет рассчитывать по этому количеству, а каждый месяц обновлять норму\n"
                         f"Поменять это поведение можно будет в настройках")
    await message.answer("Хотите ли вы прочитать инструкцию по работе с ботом?", reply_markup=schedule_keys)
    await Registration.instruction.set()


async def schedule_no(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mode'] = 2
    await message.answer("Введите количество рабочих дней в этом месяце:\n"
                         "Далее это можно будет поменять в настройках")
    await Registration.days.set()


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите вариант.\nВы работаете в графике 5/2?",
                         reply_markup=schedule_keys)


def register_handlers_registration_schedule(dp: Dispatcher):
    dp.register_message_handler(schedule_yes, state=Registration.schedule, regexp="Да")
    dp.register_message_handler(schedule_no, state=Registration.schedule, regexp="Нет")
    dp.register_message_handler(inval, state=Registration.schedule)
