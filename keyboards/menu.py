from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Добавить рабочее время")
b2 = KeyboardButton("Посчитать ПЛ")
b3 = KeyboardButton("Добавить оборот")
b4 = KeyboardButton("Контакты")
b5 = KeyboardButton("Отчёты")
b6 = KeyboardButton("Посл. данные")
b7 = KeyboardButton("Настройки")
b8 = KeyboardButton("Инструкции")
b9 = KeyboardButton("Репорт")


menu_keys = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keys.add(b1).add(b2).add(b3).row(b4, b5).row(b6, b7).row(b8, b9)
