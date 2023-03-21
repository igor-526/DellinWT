from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Обычный день")
b2 = KeyboardButton("Выход в выходной")
b3 = KeyboardButton("Выход в праздничный")


day_keys = ReplyKeyboardMarkup(resize_keyboard=True)
day_keys.add(b1).add(b2).add(b3)