from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import db_api
from keyboards import menu_keys
from handlers.contacts.fsmclass import Contacts
from handlers.commands.fsmclass import Menu


async def show(message: types.Message, state: FSMContext):
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


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


def register_handlers_contacts_show(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Contacts.select, regexp="Отмена")
    dp.register_message_handler(show, state=Contacts.select)
