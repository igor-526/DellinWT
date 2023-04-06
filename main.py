from aiogram.utils import executor
from funcs import add_auto, add_contacts
from models import on_dbstartup
from create_bot import dp



async def on_startup(_):
    await on_dbstartup()
    await add_auto.add_auto()
    await add_contacts.add_contacts()

if __name__ == "__main__":
    from handlers import calc_fuel, commands, registration, add_time, contacts
    calc_fuel.register_handlers_calc_fuel(dp)
    commands.register_handlers_commands(dp)
    registration.register_handlers_registration(dp)
    add_time.register_handlers_add_time(dp)
    contacts.register_handlers_contacts(dp)
    executor.start_polling(dp, on_startup=on_startup)
