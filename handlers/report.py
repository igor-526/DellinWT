from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import menu_keys
from create_bot import bot


class Reportissue(StatesGroup):
    report = State()


async def send_report(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    else:
        await bot.send_message(394394166, f'{message.from_user.id}\n\n{message.text}')
        await message.answer('Cообщение отправлено разработчику!\nОгромное спасибо за репорт!\n'
                             'Выберите действие:',
                             reply_markup=menu_keys)
        await state.finish()

def register_handlers_reportissue(dp: Dispatcher):
    dp.register_message_handler(send_report, state=Reportissue.report)