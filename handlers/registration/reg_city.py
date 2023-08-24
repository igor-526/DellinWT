from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import db_api
from keyboards import city_keys, base_keys
from handlers.registration.fsmclass import Registration


async def city(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['city'] = int(await db_api.city_id(message.text))
            await message.answer("Отлично! С городом определились\nТеперь выберите ваш ОСП",
                                    reply_markup=await base_keys(data['city']))
            await Registration.base.set()
    except:
        await message.answer("К сожалению, данный город ещё не поддерживается :(\nПожалуйста, выберите из списка",
                       reply_markup=await city_keys())


def register_handlers_registration_city(dp: Dispatcher):
    dp.register_message_handler(city, state=Registration.city)
