from create_bot import bot
from keyboards import instruction_keys


async def send_inst(user_id):
    await bot.send_message(user_id, 'Держи!',
                           reply_markup=instruction_keys)
