from aiogram import types, Dispatcher
from keyboards import menu_keys, cancel_keys, city_keys, schedule_keys, settings_keys
from handlers.commands.fsmclass import Menu
from handlers.settings.fsmclass import Settings


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


async def ch_name(message: types.Message):
    await message.answer("Введите имя:", reply_markup=cancel_keys)
    await Settings.set_name.set()


async def ch_place(message: types.Message):
    await message.answer("Выберите город из списка:", reply_markup=await city_keys())
    await Settings.set_city.set()


async def ch_wd(message: types.Message):
    await message.answer("Введите количество рабочих дней в этом месяце:", reply_markup=cancel_keys)
    await Settings.set_days.set()


async def ch_mode(message: types.Message):
    await message.answer("Вы работаете в графике 5/2?", reply_markup=schedule_keys)
    await Settings.set_mode.set()


async def ch_delete(message: types.Message):
    await message.answer("ВНИМАНИЕ!!!\nУДАЛЕНИЕ ПРОФИЛЯ ПРИВЕДЁТ К ПОТЕРЕ ВСЕХ ДАННЫХ\n"
                         "Вы действительно хотите удалить профиль?", reply_markup=schedule_keys)
    await Settings.del_profile.set()


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:",
                         reply_markup=settings_keys)


def register_handlers_settings_menu(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Settings.sets, regexp="Меню")
    dp.register_message_handler(ch_name, state=Settings.sets, regexp="Поменять имя")
    dp.register_message_handler(ch_place, state=Settings.sets, regexp="Поменять город/ОСП")
    dp.register_message_handler(ch_wd, state=Settings.sets, regexp="Поменять норму раб. дней")
    dp.register_message_handler(ch_mode, state=Settings.sets, regexp="Поменять режим")
    dp.register_message_handler(ch_delete, state=Settings.sets, regexp="Удалить профиль")
    dp.register_message_handler(inval, state=Settings.sets)
