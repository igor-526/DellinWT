from aiogram import types, Dispatcher
import db_api
from keyboards import menu_keys, pos_keys, cancel_keys, report_keys, city_keys, settings_keys
from handlers.calc_fuel import Calculate
from handlers.add_time import Addtime
from handlers.contacts import Contacts
from handlers.reports import Reports
from handlers.registration import Registration
from handlers.settings import Settings
from handlers.turnover import Turnover
from handlers.report import Reportissue
from funcs import gen_profile, send_inst


async def command_start(message: types.Message):
    await message.reply("Привет\n"
                        "Данный бот создан водителем деловых линий для упрощения вычислений "
                        "водителя деловых линий!\n"
                        "Должен предупредить, что введённые данные могут быть собраны для ведения журнала рабочего "
                        "времени или топлива. А так же для статистики\n"
                        "Поэтому, продолжая использование бота, Вы даёте согласие на обработку персональных данных :)")
    await message.answer("Из какого вы города?", reply_markup=await city_keys())
    await Registration.city.set()


async def menu(message: types.Message):
    if await db_api.chk_user(int(message.from_user.id)):
        await message.answer("Выберите действие:", reply_markup=menu_keys)
    else:
        await message.reply("Привет)\n"
                            "Для начала работы с ботом нужно ввести команду /start")


async def comm(message: types.Message):
    if await db_api.chk_user(int(message.from_user.id)):
        if message.text == "Посчитать ПЛ":
            await Calculate.s_odometer.set()
            await message.answer("Функция позволяет быстро посчитать значения для топлива по путевому листу!")
            await message.answer("Пожалуйста, введите начальный пробег:", reply_markup=cancel_keys)

        elif message.text == "Добавить рабочее время":
                await message.answer("Во сколько по путевому листу вы начали работать?", reply_markup=cancel_keys)
                await Addtime.s_time.set()

        elif message.text == "Настройки":
            msg = await gen_profile(message.from_user.id)
            await message.answer(msg, reply_markup=settings_keys)
            await Settings.sets.set()

        elif message.text == "Отчёты":
            await message.answer("Выберите тип отчёта:", reply_markup=report_keys)
            await Reports.select.set()

        elif message.text == "Контакты":
            await Contacts.select.set()
            await message.answer("Кто Вам нужен?", reply_markup=pos_keys)

        elif message.text == "Добавить оборот":
            await Turnover.add.set()
            await message.answer("Введите оборот:", reply_markup=cancel_keys)

        elif message.text == "Инструкции":
            await send_inst(message.from_user.id)

        elif message.text == "Репорт":
            await Reportissue.report.set()
            await message.answer("Нашли баг?\nЕсть предложение?\n"
                                 "Хотите поблагодарить разраба?\nНапишите своё сообщение и "
                                 "я обязательно его передам! Но только без картнок", reply_markup=cancel_keys)

        else:
            await message.answer("Выберите действие:", reply_markup=menu_keys)
    else:
        await message.reply("Привет)\n"
                            "Для начала работы с ботом нужно ввести команду /start")


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(menu, commands=['Меню'])
    dp.register_message_handler(comm)
