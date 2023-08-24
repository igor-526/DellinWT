from aiogram import types, Dispatcher
import db_api
from keyboards import settings_keys, schedule_keys
from funcs import gen_profile
from handlers.settings.fsmclass import Settings
from aiogram.dispatcher import FSMContext


async def del_profile(message: types.Message, state: FSMContext):
    await db_api.del_user(message.from_user.id)
    await message.answer(":(")
    await state.finish()


async def cancel(message: types.Message):
    msg = await gen_profile(message.from_user.id)
    await message.answer(msg, reply_markup=settings_keys)
    await Settings.sets.set()


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите действие:", reply_markup=schedule_keys)


def register_handlers_settings_delete(dp: Dispatcher):
    dp.register_message_handler(del_profile, state=Settings.del_profile, regexp="Да")
    dp.register_message_handler(cancel, state=Settings.del_profile, regexp="Нет")
    dp.register_message_handler(inval, state=Settings.del_profile)
