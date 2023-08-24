from aiogram import types, Dispatcher
import db_api
from keyboards import menu_keys, pos_keys, cancel_keys, report_keys, city_keys, settings_keys
from handlers.calc_fuel.fsmclass import Calculate
from handlers.add_time import Addtime
from handlers.contacts import Contacts
from handlers.reports import Reports
from handlers.registration import Registration
from handlers.settings import Settings
from handlers.turnover import Turnover
from handlers.report import Reportissue
from funcs import gen_profile, send_inst
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
import time

class Menu(StatesGroup):
    msgall = State()



async def command_start(message: types.Message, state: FSMContext):
    if not await db_api.chk_user(int(message.from_user.id)):
        await message.reply("Привет\n"
                            "Данный бот создан водителем деловых линий для упрощения вычислений "
                            "водителя деловых линий!\n"
                            "Должен предупредить, что введённые данные могут быть собраны для ведения журнала рабочего "
                            "времени или топлива. А так же для статистики\n"
                            "Поэтому, продолжая использование бота, Вы даёте согласие на обработку персональных данных :)")
        await message.answer("Из какого вы города?", reply_markup=await city_keys())
        await Registration.city.set()
    else:
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        await state.finish()

async def chkusr(message: types.Message, state: FSMContext):
    if await db_api.chk_user(int(message.from_user.id)):
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        await state.finish()
    else:
        await message.reply("Привет)\n"
                            "Для начала работы с ботом нужно ввести команду /start")


async def m_calc_fuel(message: types.Message):
    await Calculate.s_odometer.set()
    await message.answer("Функция позволяет быстро посчитать значения для топлива по путевому листу!")
    await message.answer("Пожалуйста, введите начальный пробег:", reply_markup=cancel_keys)


async def m_add_wt(message: types.Message):
    await message.answer("Во сколько по путевому листу вы начали работать?", reply_markup=cancel_keys)
    await Addtime.s_time.set()


async def m_settings(message: types.Message):
    msg = await gen_profile(message.from_user.id)
    await message.answer(msg, reply_markup=settings_keys)
    await Settings.sets.set()


async def m_reports(message: types.Message):
    await message.answer("Выберите тип отчёта:", reply_markup=report_keys)
    await Reports.select.set()


async def m_contacts(message: types.Message):
    await Contacts.select.set()
    await message.answer("Кто Вам нужен?", reply_markup=pos_keys)


async def m_turnover(message: types.Message):
    await Turnover.add.set()
    await message.answer("Введите оборот:", reply_markup=cancel_keys)


async def m_instructions(message: types.Message):
    await send_inst(message.from_user.id)


async def m_report(message: types.Message):
    await Reportissue.report.set()
    await message.answer("Нашли баг?\nЕсть предложение?\n"
                         "Хотите поблагодарить разраба?\nНапишите своё сообщение и "
                         "я обязательно его передам! Но только без картнок", reply_markup=cancel_keys)


async def m_last(message: types.Message):
    user = await db_api.chk_user(message.from_user.id)
    if user.last_km:
        await message.answer(f'Одометр: {user.last_km}\nТопливо:{user.last_fuel}')
    else:
        await message.answer("Последних данных нет\nИспользуйте функцию для рассчёта путевого листа")


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


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(chkusr, commands=['reset'], state='*')
    dp.register_message_handler(message_to_all, commands=['msgall'])
    dp.register_message_handler(message_to_all_send, state=Menu.msgall)
    dp.register_message_handler(m_calc_fuel, regexp='Посчитать ПЛ')
    dp.register_message_handler(m_add_wt, regexp='Добавить рабочее время')
    dp.register_message_handler(m_settings, regexp='Настройки')
    dp.register_message_handler(m_reports, regexp='Отчёты')
    dp.register_message_handler(m_contacts, regexp='Контакты')
    dp.register_message_handler(m_turnover, regexp='Добавить оборот')
    dp.register_message_handler(m_instructions, regexp='Инструкции')
    dp.register_message_handler(m_report, regexp='Репорт')
    dp.register_message_handler(m_last, regexp='Посл. данные')
    dp.register_message_handler(chkusr)
