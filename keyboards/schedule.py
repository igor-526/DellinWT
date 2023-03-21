from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("5/2")
b2 = KeyboardButton("2/2")


schedule_keys = ReplyKeyboardMarkup(resize_keyboard=True)
schedule_keys.add(b1).add(b2)