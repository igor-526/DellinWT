from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Посчитать топливо")
b2 = KeyboardButton("Добавить рабочее время")
b3 = KeyboardButton("Настройки")


menu_keys = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keys.add(b1).add(b2).add(b3)
