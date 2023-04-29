from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Добавить рабочее время")
b2 = KeyboardButton("Посчитать ПЛ")
b3 = KeyboardButton("Добавить оборот")
b4 = KeyboardButton("Контакты")
b5 = KeyboardButton("Отчёты")
b6 = KeyboardButton("Настройки")
b7 = KeyboardButton("Инструкции")
b8 = KeyboardButton("Репорт")


menu_keys = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keys.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6).add(b7).add(b8)
