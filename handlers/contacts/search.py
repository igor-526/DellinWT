from aiogram import types, Dispatcher
import db_api
from keyboards import menu_keys, cancel_keys
from handlers.contacts.fsmclass import Contacts
from handlers.commands.fsmclass import Menu


async def search(message: types.Message):
    await message.answer("Поиск:", reply_markup=cancel_keys)
    await Contacts.search.set()


async def search_q(message: types.Message):
    if message.text == "Отмена":
        await Menu.menu.set()
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
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        await Menu.menu.set()
    else:
        await message.answer("Ничего не найдено :(\n\n"
                             "Выберите действие:", reply_markup=menu_keys)
        await Menu.menu.set()


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


def register_handlers_contacts_search(dp: Dispatcher):
    dp.register_message_handler(search, state=Contacts.select, regexp="Поиск")
    dp.register_message_handler(cancel, state=Contacts.select, regexp="Отмена")
    dp.register_message_handler(search_q, state=Contacts.search)
