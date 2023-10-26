from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Добавить запись")
b2 = KeyboardButton("Изменить дату")
b3 = KeyboardButton("Отмена")

confirm_keys = ReplyKeyboardMarkup(resize_keyboard=True)
confirm_keys.add(b1).add(b2).add(b3)
