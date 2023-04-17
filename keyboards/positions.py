from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Логист")
b2 = KeyboardButton("АТП Армада")
b3 = KeyboardButton("Менеджер по транспорту")
b4 = KeyboardButton("Претензионный отдел")
b5 = KeyboardButton("Склад")
b6 = KeyboardButton("Кассир")
b7 = KeyboardButton("Распилка Армада")
bsearch = KeyboardButton("Поиск")
bcancel = KeyboardButton("Отмена")


pos_keys = ReplyKeyboardMarkup(resize_keyboard=True)
pos_keys.add(bsearch).add(b2).add(b6).add(b1).add(b3).add(b4).add(b7).add(b5).add(bcancel)