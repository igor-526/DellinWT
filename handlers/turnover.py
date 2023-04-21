from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import db_api
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import menu_keys, cancel_keys, schedule_keys
from datetime import date


class Turnover(StatesGroup):
    add = State()
    confirm = State()


async def add(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
    else:
        try:
            turnover = float(message.text)
            if turnover > 0:
                async with state.proxy() as data:
                    data['turnover'] = turnover
                await message.answer(f"Вы действительно хотите добавить оборот: {turnover}", reply_markup=schedule_keys)
                await Turnover.confirm.set()
            else: raise
        except:
            await message.answer("Я вас не понимаю :(\nПожалуйста, введите числовое значение оборота",
                                 reply_markup=cancel_keys)


async def confirm(message: types.Message, state: FSMContext):
    if message.text == "Нет":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
    elif message.text == "Да":
        async with state.proxy() as data:
            await db_api.add_turnover(message.from_user.id, data['turnover'], date.today())
        await state.finish()
        await message.answer("Оборот успешно добавлен!\nВыберите действие:", reply_markup=menu_keys)
    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:",
                             reply_markup=schedule_keys)

def register_handlers_turnover(dp: Dispatcher):
    dp.register_message_handler(add, state=Turnover.add)
    dp.register_message_handler(confirm, state=Turnover.confirm)