from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Предыдущий месяц")
b2 = KeyboardButton("Другой месяц")
b3 = KeyboardButton("Удалить запись")
b4 = KeyboardButton("Меню")

reported_keys = ReplyKeyboardMarkup(resize_keyboard=True)
reported_keys.add(b1).add(b2).add(b3).add(b4)
