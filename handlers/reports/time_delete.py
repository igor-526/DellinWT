from aiogram import types, Dispatcher
from keyboards import menu_keys, reported_keys, del_confirm_keys
from handlers.commands.fsmclass import Menu
from handlers.reports.fsmclass import Reports
from aiogram.dispatcher import FSMContext
import db_api


async def menu(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


async def delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await db_api.del_time(data["res"]["ids"])
    await message.answer("Записи успешно удалены", reply_markup=reported_keys)
    await Reports.time_reported.set()


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:", reply_markup=del_confirm_keys)


def register_handlers_reports_time_delete(dp: Dispatcher):
    dp.register_message_handler(delete, state=Reports.time_del_confirm, regexp="Удалить записи")
    dp.register_message_handler(menu, state=Reports.time_del_confirm, regexp="Меню")
    dp.register_message_handler(inval, state=Reports.time_del_confirm)
