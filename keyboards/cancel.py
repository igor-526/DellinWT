from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Отмена")

cancel_keys = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keys.add(b1)
