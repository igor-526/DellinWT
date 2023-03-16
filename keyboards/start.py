from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("/Меню")

start_keys = ReplyKeyboardMarkup(resize_keyboard=True)
start_keys.add(b1)
