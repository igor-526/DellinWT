from aiogram import types, Dispatcher
import db_api
from keyboards import cancel_keys, settings_keys
from funcs import gen_profile
from handlers.settings.fsmclass import Settings


async def set_name(message: types.Message):
    try:
        await db_api.upd_user(message.from_user.id, name=message.text)
        await message.answer("Имя успешно изменено!")
        msg = await gen_profile(message.from_user.id)
        await message.answer(msg, reply_markup=settings_keys)
        await Settings.sets.set()
    except:
        await message.answer("Что-то пошло не так :(\nПопробуйте ещё раз", reply_markup=cancel_keys)


async def cancel(message: types.Message):
    msg = await gen_profile(message.from_user.id)
    await message.answer(msg, reply_markup=settings_keys)
    await Settings.sets.set()


def register_handlers_settings_name(dp: Dispatcher):
    dp.register_message_handler(cancel, state=Settings.set_name, regexp="Отмена")
    dp.register_message_handler(set_name, state=Settings.set_name)
