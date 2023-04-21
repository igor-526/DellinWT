from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Рабочее время")
b2 = KeyboardButton("Поездки")
b3 = KeyboardButton("Оборот")
b4 = KeyboardButton("Отмена")

report_keys = ReplyKeyboardMarkup(resize_keyboard=True)
report_keys.add(b1).add(b2).add(b3).add(b4)