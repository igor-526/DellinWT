from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Посчитать топливо")
b2 = KeyboardButton("Добавить рабочее время")
b3 = KeyboardButton("Настройки")
b4 = KeyboardButton("Отчёты")
b5 = KeyboardButton("Полезные контакты")


menu_keys = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keys.add(b1).add(b2).add(b3).add(b4).add(b5)
