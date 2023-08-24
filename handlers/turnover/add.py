from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_keys, cancel_keys, schedule_keys
from handlers.turnover.fsmclass import Turnover
from handlers.commands.fsmclass import Menu


async def add(message: types.Message, state: FSMContext):
    try:
        turnover = float(message.text)
        if turnover > 0:
            async with state.proxy() as data:
                data['turnover'] = turnover
            await message.answer(f"Вы действительно хотите добавить оборот: {turnover}", reply_markup=schedule_keys)
            await Turnover.confirm.set()
        else:
            raise
    except:
        await message.answer("Я вас не понимаю :(\nПожалуйста, введите числовое значение оборота",
                             reply_markup=cancel_keys)


async def cancel(message: types.Message):
    await Menu.menu.set()
    await message.answer("Выберите действие:", reply_markup=menu_keys)


def register_handlers_turnover_add(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Turnover.add, regexp="Отмена")
    dp.register_message_handler(add, state=Turnover.add)
