from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import db_api
from keyboards import base_keys, schedule_keys
from handlers.registration.fsmclass import Registration


async def base(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['base'] = int(await db_api.base_id(message.text))
            await message.answer("Отлично! С базой определились!\nПодскажите, вы работаете в графике 5/2?",
                                 reply_markup=schedule_keys)
            await Registration.schedule.set()
    except:
        async with state.proxy() as data:
            await message.answer("К сожалению, данное ОСП ещё не поддерживается :(\nПожалуйста, выберите из списка",
                                 reply_markup=await base_keys(data['city']))


def register_handlers_registration_base(dp: Dispatcher):
    dp.register_message_handler(base, state=Registration.base)
