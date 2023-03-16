from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
import db_api

class Register(StatesGroup):
    number = State()
    time = State()


@dp.message_handler(state=Register.number)
async def process_number(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['number'] = int(message.text)
        await Register.time.set()
        await message.answer("Отлично! Теперь выберите или введите свою норму часов в месяц:")
    except:
        await message.answer("Вы ввели какую то хуйню. Попробуйте ещё раз")


@dp.message_handler(state=Register.time)
async def process_time(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['time'] = int(message.text)
            adddict = dict(data)
            await db_api.add_user(adddict['number'], adddict['time'], int(message.from_user.id))
        await state.finish()
        await message.answer("Отлично! Теперь вы можете пользоваться ботом!")
    except:
        await message.answer("Вы ввели какую то хуйню. Попробуйте ещё раз")

def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(process_number, state=Register.number)
    dp.register_message_handler(process_time, state=Register.time)