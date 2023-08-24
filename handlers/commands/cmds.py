from aiogram import types, Dispatcher
import db_api
from keyboards import menu_keys, city_keys, cancel_keys
from handlers.registration.fsmclass import Registration
from handlers.issuereport.fsmclass import Reportissue
from handlers.commands.fsmclass import Menu
from aiogram.dispatcher import FSMContext
from create_bot import bot
import time


async def command_start(message: types.Message):
    if not await db_api.chk_user(int(message.from_user.id)):
        await message.reply("Привет\n"
                            "Данный бот создан водителем деловых линий для упрощения вычислений "
                            "водителя деловых линий!\n"
                            "Должен предупредить, что введённые данные могут быть собраны для ведения журнала рабочего "
                            "времени или топлива. А так же для статистики\n"
                            "Поэтому, продолжая использование бота, Вы даёте согласие на "
                            "обработку персональных данных :)")
        await message.answer("Из какого вы города?", reply_markup=await city_keys())
        await Registration.city.set()
    else:
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        await Menu.menu.set()


async def chkusr(message: types.Message):
    if await db_api.chk_user(int(message.from_user.id)):
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        await Menu.menu.set()
    else:
        await message.reply("Привет)\n"
                            "Для начала работы с ботом нужно ввести команду /start")


async def message_to_all(message: types.Message):
    if message.from_user.id == 394394166:
        await message.answer('Введите сообщение:')
        await Menu.msgall.set()
    else:
        await message.answer("Служебная функция доступна только администраторам")


async def message_to_all_send(message: types.Message, state: FSMContext):
    ids = await db_api.sel_all_users()
    await message.answer(f"Сообщение отправляется {len(ids)} пользователям")
    for user in ids:
        try:
            await bot.send_message(user, message.text)
            time.sleep(0.2)
        except:
            pass
    await message.answer("Сообщение отправлено")
    await state.finish()


async def issuereport(message: types.Message):
    await Reportissue.report.set()
    await message.answer("Нашли баг?\nЕсть предложение?\n"
                         "Хотите поблагодарить разраба?\nНапишите своё сообщение и "
                         "я обязательно его передам! Но только без картнок", reply_markup=cancel_keys)


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_message_handler(chkusr, commands=['reset'], state='*')
    dp.register_message_handler(issuereport, commands=['report'], state='*')
    dp.register_message_handler(message_to_all, commands=['msgall'], state=Menu.menu)
    dp.register_message_handler(message_to_all_send, state=Menu.msgall)
    dp.register_message_handler(chkusr)
