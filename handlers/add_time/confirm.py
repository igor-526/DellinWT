from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, cancel_keys
from funcs import log
from handlers.add_time.fsmclass import Addtime
from handlers.commands.fsmclass import Menu
import db_api


async def add_note(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await db_api.add_time(int(message.from_user.id),
                              data['start'],
                              data['end'],
                              float(data["ttl"]["c"]),
                              data["ttl"]['totalfloat'])
    await message.answer("Запись добавлена\n"
                         "Выберите действие:", reply_markup=menu_keys)
    await log(message.from_user.id, "Added worktime to DB", str(data))
    await Menu.menu.set()


async def ch_date(message: types.Message):
    await Addtime.change_date.set()
    await message.answer("Пожалуйста, введите дату в формате ДД.ММ", reply_markup=cancel_keys)


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


async def inval(message: types.Message):
    await message.answer("Я так не понимаю :(\n"
                         "Пожалуйста, выберите действие на клавиатуре")


def register_handlers_at_confirm(dp: Dispatcher):
    dp.register_message_handler(add_note, state=Addtime.confirm, regexp="Добавить запись")
    dp.register_message_handler(ch_date, state=Addtime.confirm, regexp="Изменить дату")
    dp.register_message_handler(cancel, state=Addtime.confirm, regexp='Отмена')
    dp.register_message_handler(inval, state=Addtime.confirm)
