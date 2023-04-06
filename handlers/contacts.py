from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import db_api
from create_bot import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import auto_keys
from funcs import calc_fuel
from keyboards import menu_keys
from pprint import pprint

class Contacts(StatesGroup):
    select = State()

async def show(message: types.Message, state: FSMContext):
    if str(message.text) == "Меню":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
    else:
        contacts = await db_api.show_contacts(str(message.text))
        counter = 0
        msg = ''
        print(len(contacts))
        for contact in contacts:
            msg += f'{contact.last_name} {contact.first_name} {contact.middle_name}\n' \
                   f'<b>{contact.comment}</b> | {contact.phone}\n' \
                   f'WhatsApp: wa.me/{contact.phone}\n\n'
            counter += 1
            if counter == 8:
                await message.answer(msg, parse_mode='HTML')
                counter = 0
                msg = ''
        await message.answer(msg, parse_mode='HTML')
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)

def register_handlers_contacts(dp: Dispatcher):
    dp.register_message_handler(show, state=Contacts.select)