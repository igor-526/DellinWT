from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

b1 = InlineKeyboardButton(text="Коротко обо всём", url=config.instruction_all)
b2 = InlineKeyboardButton(text="О боте", url=config.instruction_about)

instruction_keys = InlineKeyboardMarkup()
instruction_keys.add(b1).add(b2)