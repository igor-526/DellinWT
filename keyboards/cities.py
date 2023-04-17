from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import db_api

async def city_keys():
    list = await db_api.show_cities()
    keys = ReplyKeyboardMarkup(resize_keyboard=True)
    for city in list:
        button = KeyboardButton(city.name)
        keys.add(button)
    return keys