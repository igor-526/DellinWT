from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Да")
b2 = KeyboardButton("Нет")

schedule_keys = ReplyKeyboardMarkup(resize_keyboard=True)
schedule_keys.add(b1).add(b2)
