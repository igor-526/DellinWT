from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
import db_api
from keyboards import start_keys
from keyboards import menu_keys
from handlers.calc_fuel import Calculate

async def command_start(message : types.Message):
    await message.reply("Привет\n"
                        "Данный бот создан водителем деловых линий для упрощения вычислений"
                        "водителя деловых линий!\n"
                        "Должен предупредить, что введённые данные могут быть собраны для ведения журнала рабочего"
                        "времени или топлива. А так же для статистики\n"
                        "Поэтому, продолжая использование бота, Вы даёте согласие на обработку персональных данных :)",
                        reply_markup=start_keys)
    await db_api.add_user(int(message.from_user.id), 0, 0)


async def menu(message : types.Message):
    if await db_api.chk_user(int(message.from_user.id)):
        await message.answer("Выберите действие:", reply_markup=menu_keys)
    else:
        await message.reply("Привет)\n"
                            "Для начала работы с ботом нужно ввести команду /start")


async def comm(message : types.Message):
    if await db_api.chk_user(int(message.from_user.id)):
        if str(message.text) == "Посчитать топливо":
            await Calculate.s_odometer.set()
            await message.answer("Функция позволяет быстро посчитать значения для топлива по путевому листу!")
            await message.answer("Пожалуйста, введите начальный пробег:")
        elif str(message.text) == "Добавить рабочее время":
            await message.answer("К сожалению, данная функция ещё не реализована :(")
        elif str(message.text) == "Настройки":
            await message.answer("К сожалению, данная функция ещё не реализована :(")
        else:
            await message.answer("Выберите действие:", reply_markup=menu_keys)
    else:
        await message.reply("Привет)\n"
                            "Для начала работы с ботом нужно ввести команду /start")


def register_handlers_commands (dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(menu, commands=['Меню'])
    dp.register_message_handler(comm)