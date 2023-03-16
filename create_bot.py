from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = '6273571621:AAGh9hAmIwqvzsRt0Ke1Ys4RdZ1LQRtu-B8'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)