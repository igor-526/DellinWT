from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Нет")
b2 = KeyboardButton("Отмена")

refuel_keys = ReplyKeyboardMarkup(resize_keyboard=True)
refuel_keys.add(b1).add(b2)