from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Удалить записи")
b2 = KeyboardButton("Меню")

del_confirm_keys = ReplyKeyboardMarkup(resize_keyboard=True)
del_confirm_keys.add(b1).add(b2)