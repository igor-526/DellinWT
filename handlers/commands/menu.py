from aiogram import types, Dispatcher
import db_api
from keyboards import pos_keys, cancel_keys, report_keys, settings_keys
from handlers.calc_fuel.fsmclass import Calculate
from handlers.reports.fsmclass import Reports
from handlers.settings.fsmclass import Settings
from handlers.issuereport.fsmclass import Reportissue
from handlers.commands.fsmclass import Menu
from handlers.add_time.fsmclass import Addtime
from handlers.turnover.fsmclass import Turnover
from handlers.contacts.fsmclass import Contacts
from funcs import gen_profile, send_inst


async def m_calc_fuel(message: types.Message):
    await message.answer("Функция позволяет быстро посчитать значения для топлива по путевому листу!")
    await message.answer("Пожалуйста, введите начальный пробег:", reply_markup=cancel_keys)
    await Calculate.s_odometer.set()


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
        await message.answer(f'Одометр: {user.last_km} км\nТопливо:{ user.last_fuel} л')
    else:
        await message.answer("Последних данных нет\nИспользуйте функцию для рассчёта путевого листа")


def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(m_calc_fuel, regexp='Посчитать ПЛ', state=Menu.menu)
    dp.register_message_handler(m_add_wt, regexp='Добавить рабочее время', state=Menu.menu)
    dp.register_message_handler(m_settings, regexp='Настройки', state=Menu.menu)
    dp.register_message_handler(m_reports, regexp='Отчёты', state=Menu.menu)
    dp.register_message_handler(m_contacts, regexp='Контакты', state=Menu.menu)
    dp.register_message_handler(m_turnover, regexp='Добавить оборот', state=Menu.menu)
    dp.register_message_handler(m_instructions, regexp='Инструкции', state=Menu.menu)
    dp.register_message_handler(m_report, regexp='Репорт', state=Menu.menu)
    dp.register_message_handler(m_last, regexp='Посл. данные', state=Menu.menu)
