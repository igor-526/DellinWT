from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import db_api


async def base_keys(city):
    list = await db_api.show_bases(city)
    keys = ReplyKeyboardMarkup(resize_keyboard=True)
    for base in list:
        button = KeyboardButton(base.name)
        keys.add(button)
    return keys
