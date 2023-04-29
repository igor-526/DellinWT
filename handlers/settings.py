from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import db_api
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import menu_keys, cancel_keys, city_keys, base_keys, schedule_keys, settings_keys
from funcs import get_wdays, gen_profile
from datetime import date


class Settings(StatesGroup):
    sets = State()
    set_name = State()
    set_city = State()
    set_base = State()
    set_days = State()
    set_mode = State()
    del_profile = State()


async def sets(message: types.Message, state: FSMContext):
    if message.text == "Меню":
        await message.answer("Выберите действие:", reply_markup=menu_keys)
        await state.finish()
        return
    elif message.text == "Поменять имя":
        await message.answer("Введите имя:", reply_markup=cancel_keys)
        await Settings.set_name.set()
    elif message.text == "Поменять город/ОСП":
        await message.answer("Выберите город из списка:", reply_markup=await city_keys())
        await Settings.set_city.set()
    elif message.text == "Поменять норму раб. дней":
        await message.answer("Введите количество рабочих дней в этом месяце:", reply_markup=cancel_keys)
        await Settings.set_days.set()
    elif message.text == "Поменять режим":
        await message.answer("Вы работаете в графике 5/2?", reply_markup=schedule_keys)
        await Settings.set_mode.set()
    elif message.text == "Удалить профиль":
        await message.answer("ВНИМАНИЕ!!!\nУДАЛЕНИЕ ПРОФИЛЯ ПРИВЕДЁТ К ПОТЕРЕ ВСЕХ ДАННЫХ\n"
                             "Вы действительно хотите удалить профиль?", reply_markup=schedule_keys)
        await Settings.del_profile.set()
    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие из списка:",
                             reply_markup=settings_keys)


async def set_name(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        msg = await gen_profile(message.from_user.id)
        await message.answer(msg, reply_markup=settings_keys)
        await Settings.sets.set()
    else:
        try:
            await db_api.upd_user(message.from_user.id, name=message.text)
            await message.answer("Имя успешно изменено!")
            msg = await gen_profile(message.from_user.id)
            await message.answer(msg, reply_markup=settings_keys)
            await Settings.sets.set()
        except:
            await message.answer("Что-то пошло не так :(\nПопробуйте ещё раз", reply_markup=cancel_keys)


async def set_city(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['city'] = int(await db_api.city_id(message.text))
            await message.answer("Отлично! С городом определились\nТеперь выберите ваш ОСП",
                                 reply_markup=await base_keys(data['city']))
            await Settings.set_base.set()
    except:
        await message.answer("К сожалению, данный город ещё не поддерживается :(\nПожалуйста, выберите из списка",
                             reply_markup=await city_keys())


async def set_base(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['base'] = int(await db_api.base_id(message.text))
            await db_api.upd_user(message.from_user.id, city=data['city'], base=data['base'])
            await message.answer("Отлично! С базой определились!\nНастройки успешно изменены!",
                                 reply_markup=settings_keys)
            msg = await gen_profile(message.from_user.id)
            await message.answer(msg, reply_markup=settings_keys)
            await Settings.sets.set()
            await Settings.sets.set()
    except:
        async with state.proxy() as data:
            await message.answer("К сожалению, данное ОСП ещё не поддерживается :(\nПожалуйста, выберите из списка",
                                 reply_markup=await base_keys(data['city']))


async def set_days(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        msg = await gen_profile(message.from_user.id)
        await message.answer(msg, reply_markup=settings_keys)
        await Settings.sets.set()
    else:
        try:
            days = int(message.text)
            if 1 <= days <= 31:
                hours = days * 8
                await db_api.upd_user(message.from_user.id, workdays=days)
                await message.answer(f"В этом месяце у вас {days} рабочих дней\n"
                                     f"Это {hours} часов!\n"
                                     f"Далее бот будет рассчитывать по этому количеству, а каждый месяц предлагать "
                                     f"обновлять норму\n", reply_markup=settings_keys)
                msg = await gen_profile(message.from_user.id)
                await message.answer(msg, reply_markup=settings_keys)
                await Settings.sets.set()
            else:
                await message.answer("Я вас не понимаю :(\nПожалуйста, введите количество рабочих дней по плану вашего "
                                     "производственного календаря", reply_markup=cancel_keys)
        except:
            await message.answer("Я вас не понимаю :(\nПожалуйста, введите количество рабочих дней по плану вашего "
                                 "производственного календаря", reply_markup=cancel_keys)


async def set_mode(message: types.Message, state: FSMContext):
    if message.text == "Да":
        days = await get_wdays(date.today().month, date.today().year)
        await db_api.upd_user(message.from_user.id, mode=1, workdays=days['work'])
        await message.answer(f"В этом месяце у вас {days['work']} рабочих дней\n"
                             f"Это {days['hours']} часов!\n"
                             f"Далее бот будет рассчитывать по этому количеству, а каждый месяц обновлять норму\n"
                             f"Поменять это поведение можно будет в настройках")
        msg = await gen_profile(message.from_user.id)
        await message.answer(msg, reply_markup=settings_keys)
        await Settings.sets.set()

    elif message.text == "Нет":
        await db_api.upd_user(message.from_user.id, mode=2)
        await message.answer("Теперь бот будет каждый месяц спрашивать количество рабочих дней по плану\n"
                             "Поменять количество можно будет в любой момент в настройках")
        msg = await gen_profile(message.from_user.id)
        await message.answer(msg, reply_markup=settings_keys)
        await Settings.sets.set()

    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите вариант.\nВы работаете в графике 5/2?",
                             reply_markup=schedule_keys)


async def del_profile(message: types.Message, state: FSMContext):
    if message.text == "Нет":
        msg = await gen_profile(message.from_user.id)
        await message.answer(msg, reply_markup=settings_keys)
        await Settings.sets.set()
    elif message.text == "Да":
        await db_api.del_user(message.from_user.id)
        await message.answer(":(")
        await state.finish()
    else:
        await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие:", reply_markup=schedule_keys)


def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(sets, state=Settings.sets)
    dp.register_message_handler(set_name, state=Settings.set_name)
    dp.register_message_handler(set_city, state=Settings.set_city)
    dp.register_message_handler(set_base, state=Settings.set_base)
    dp.register_message_handler(set_days, state=Settings.set_days)
    dp.register_message_handler(set_mode, state=Settings.set_mode)
    dp.register_message_handler(del_profile, state=Settings.del_profile)