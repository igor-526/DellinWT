from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from models import User, Time
from models import on_dbstartup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pprint import pprint
import db_api

TOKEN = '6273571621:AAGh9hAmIwqvzsRt0Ke1Ys4RdZ1LQRtu-B8'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Register(StatesGroup):
    number = State()
    time = State()

async def on_startup(_):
    print ("Bot started succesfully!")
    await on_dbstartup()

@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    await Register.number.set()
    await message.reply("Привет. Напиши, пожалуйста, свой табельный номер :)")

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
async def process_number(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['time'] = int(message.text)
            adddict = dict(data)
            await db_api.add_user(adddict['number'], adddict['time'])
        await state.finish()
        await message.answer("Отлично! Теперь вы можете пользоваться ботом!")
    except:
        await message.answer("Вы ввели какую то хуйню. Попробуйте ещё раз")

@dp.message_handler()
async def command_start(message : types.Message):
    await message.reply("Привет)\n"
                        "Для начала работы с ботом нужно зарегистрироваться (анонимно)\n"
                        "О своих функциях - /help")
    

executor.start_polling(dp, on_startup=on_startup)