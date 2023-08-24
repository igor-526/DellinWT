from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import db_api
from keyboards import menu_keys
from funcs import send_inst
from handlers.registration.fsmclass import Registration
from handlers.commands.fsmclass import Menu


async def instruct_no(message: types.Message, state: FSMContext):
    if message.text == "Нет":
        async with state.proxy() as data:
            await db_api.add_user(message.from_user.id, message.from_user.first_name,
                                  data['city'], data['base'], data['mode'], data['wdays']['work'])
        await message.answer("Вы успешно зарегистрировались!\nВыберите действие:", reply_markup=menu_keys)
        await Menu.menu.set()


async def instruct_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await db_api.add_user(message.from_user.id, message.from_user.first_name,
                              data['city'], data['base'], data['mode'], data['wdays']['work'])
    await send_inst(message.from_user.id)
    await message.answer("Вы успешно зарегистрировались!\nВыберите действие:", reply_markup=menu_keys)
    await state.finish()


async def inval(message: types.Message):
    await message.answer("Я вас не понимаю :(\nПожалуйста, выберите из списка")


def register_handlers_registration_instruct(dp: Dispatcher):
    dp.register_message_handler(instruct_no, state=Registration.instruction, regexp="Нет")
    dp.register_message_handler(instruct_yes, state=Registration.instruction, regexp="Да")
    dp.register_message_handler(inval, state=Registration.instruction)
