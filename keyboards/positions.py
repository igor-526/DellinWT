from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Логист")
b2 = KeyboardButton("Меню")


pos_keys = ReplyKeyboardMarkup(resize_keyboard=True)
pos_keys.add(b1).add(b2)