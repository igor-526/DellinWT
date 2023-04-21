from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Поменять имя")
b2 = KeyboardButton("Поменять город/ОСП")
b3 = KeyboardButton("Поменять норму раб. дней")
b4 = KeyboardButton("Поменять режим")
b5 = KeyboardButton("Удалить профиль")
b6 = KeyboardButton("Меню")

settings_keys = ReplyKeyboardMarkup(resize_keyboard=True)
settings_keys.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)