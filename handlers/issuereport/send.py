from aiogram import types, Dispatcher
from keyboards import menu_keys
from create_bot import bot
from handlers.issuereport.fsmclass import Reportissue
from handlers.commands.fsmclass import Menu


async def send_report(message: types.Message):
    await bot.send_message(394394166, f'{message.from_user.id}\n\n{message.text}')
    await message.answer('Cообщение отправлено разработчику!\nОгромное спасибо за репорт!\n'
                         'Выберите действие:',
                         reply_markup=menu_keys)
    await Menu.menu.set()


async def cancel(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu_keys)
    await Menu.menu.set()


def register_handlers_reportissue(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Reportissue.report, regexp="Отмена")
    dp.register_message_handler(send_report, state=Reportissue.report)
