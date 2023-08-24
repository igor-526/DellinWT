from aiogram import types, Dispatcher
import db_api
from keyboards import settings_keys, cancel_keys
from funcs import gen_profile
from handlers.settings.fsmclass import Settings


async def set_days(message: types.Message):
    try:
        days = int(message.text)
        if 1 <= days <= 31:
            hours = days * 8
            await db_api.upd_user(message.from_user.id, workdays=days)
            await message.answer(f"В этом месяце у вас {days} рабочих дней\n"
                                 f"Это {hours} часов!\n"
                                 f"Далее бот будет рассчитывать по этому количеству, а каждый месяц предлагать "
                                 f"обновлять норму\n", reply_markup=settings_keys)
            msg = await gen_profile(message.from_user.id)
            await message.answer(msg, reply_markup=settings_keys)
            await Settings.sets.set()
        else:
            await message.answer("Я вас не понимаю :(\nПожалуйста, введите количество рабочих дней по плану вашего "
                                 "производственного календаря", reply_markup=cancel_keys)
    except:
        await message.answer("Я вас не понимаю :(\nПожалуйста, введите количество рабочих дней по плану вашего "
                             "производственного календаря", reply_markup=cancel_keys)


async def cancel(message: types.Message):
    msg = await gen_profile(message.from_user.id)
    await message.answer(msg, reply_markup=settings_keys)
    await Settings.sets.set()


def register_handlers_settings_wd(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Settings.set_days, regexp="Отмена")
    dp.register_message_handler(set_days, state=Settings.set_days)

