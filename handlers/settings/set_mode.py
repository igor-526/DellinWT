from aiogram import types, Dispatcher
from handlers.settings.fsmclass import Settings
import db_api
from keyboards import schedule_keys, settings_keys
from funcs import get_wdays, gen_profile
from datetime import date


async def set_mode(message: types.Message):
    if message.text == "Да":
        days = await get_wdays(date.today().month, date.today().year)
        await db_api.upd_user(message.from_user.id, mode=1, workdays=days['work'])
        await message.answer(f"В этом месяце у вас {days['work']} рабочих дней\n"
                             f"Это {days['hours']} часов!\n"
                             f"Далее бот будет рассчитывать по этому количеству, а каждый месяц обновлять норму\n"
                             f"Поменять это поведение можно будет в настройках")
        msg = await gen_profile(message.from_user.id)
        await message.answer(msg, reply_markup=settings_keys)
        await Settings.sets.set()

    elif message.text == "Нет":
        await db_api.upd_user(message.from_user.id, mode=2)
        await message.answer("Теперь бот будет каждый месяц спрашивать количество рабочих дней по плану\n"
                             "Поменять количество можно будет в любой момент в настройках")
        msg = await gen_profile(message.from_user.id)
        await message.answer(msg, reply_markup=settings_keys)
        await Settings.sets.set()

    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите вариант.\nВы работаете в графике 5/2?",
                             reply_markup=schedule_keys)


async def cancel(message: types.Message):
    msg = await gen_profile(message.from_user.id)
    await message.answer(msg, reply_markup=settings_keys)
    await Settings.sets.set()


def register_handlers_settings_mode(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Settings.set_mode, regexp="Отмена")
    dp.register_message_handler(set_mode, state=Settings.set_mode)

