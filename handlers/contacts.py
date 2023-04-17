from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import db_api
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import menu_keys, cancel_keys


class Contacts(StatesGroup):
    select = State()
    search = State()

async def show(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    elif message.text == "Поиск":
        await Contacts.search.set()
        await message.answer("Поиск:", reply_markup=cancel_keys)
    else:
        contacts = await db_api.show_contacts(str(message.text))
        counter = 0
        msg = ''
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

async def search(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        return
    contacts = await db_api.search_contacts(str(message.text))
    counter = 0
    msg = ''
    if contacts:
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
    else:
        await state.finish()
        await message.answer("Ничего не найдено :(\n\n"
                             "Выберите действие:", reply_markup=menu_keys)

def register_handlers_contacts(dp: Dispatcher):
    dp.register_message_handler(show, state=Contacts.select)
    dp.register_message_handler(search, state=Contacts.search)