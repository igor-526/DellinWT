from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import db_api

async def auto_keys():
    list_auto = await db_api.show_auto()
    keys = ReplyKeyboardMarkup(resize_keyboard=True)
    for auto in list_auto:
        button = KeyboardButton(auto['name'])
        keys.add(button)
    return keys
