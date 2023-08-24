from aiogram import types, Dispatcher
import db_api
from keyboards import settings_keys, base_keys, city_keys
from funcs import gen_profile
from handlers.settings.fsmclass import Settings
from aiogram.dispatcher import FSMContext


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


async def cancel(message: types.Message):
    msg = await gen_profile(message.from_user.id)
    await message.answer(msg, reply_markup=settings_keys)
    await Settings.sets.set()


def register_handlers_settings_place(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Settings.set_city, regexp="Отмена")
    dp.register_message_handler(cancel, state=Settings.set_base, regexp="Отмена")
    dp.register_message_handler(set_city, state=Settings.set_city)
    dp.register_message_handler(set_base, state=Settings.set_base)

