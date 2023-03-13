from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from models import User, Time
from models import on_dbstartup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

TOKEN = '6273571621:AAGh9hAmIwqvzsRt0Ke1Ys4RdZ1LQRtu-B8'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

class F_number(StatesGroup):
    number = State()

async def on_startup(_):
    print ("Bot started succesfully!")
    await on_dbstartup()

@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    await F_number.number.set()
    await message.reply("Привет. Напиши, пожалуйста, свой табельный номер :)")

@dp.message_handler(state=F_number.number)
async def process_number(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f"Hello, {message.text}")
    

executor.start_polling(dp, on_startup=on_startup)