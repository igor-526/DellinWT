from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import schedule_keys
from handlers.registration.fsmclass import Registration


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


def register_handlers_registration_wd(dp: Dispatcher):
    dp.register_message_handler(work_days, state=Registration.days)
