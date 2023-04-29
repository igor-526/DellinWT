from create_bot import bot
from keyboards import instruction_keys

async def send_inst(id):
    await bot.send_message(id, 'Держи!',
                           reply_markup=instruction_keys)