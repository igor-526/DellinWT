from aiogram.utils import executor

import config
from funcs import add_auto, add_contacts, add_city, add_base, log
from models import db_bind, db_reset
from create_bot import dp


async def on_startup(_):
    print("Connecting to database...")
    try:
        await db_bind()
        print("Connected to database succesfully!\n")
    except:
        print("Couldn't connect to database. Please, check")
        return
    if config.resetdb == 1:
        await db_reset()
        print("DATABASE WAS RESETED\n")

    if config.upd_city == 1:
        print("Updating cities...")
        try:
            await add_city.add_city()
            print("Updated succesfully!\n")
        except:
            print("Error. Please, check fixtures")
            return

    if config.upd_base == 1:
        print("Updating bases...")
        try:
            await add_base.add_base()
            print("Updated succesfully!\n")
        except:
            print("Error. Please, check fixtures")
            return

    if config.upd_auto == 1:
        print("Updating auto...")
        try:
            await add_auto.add_auto()
            print("Updated succesfully!\n")
        except:
            print("Error. Please, check fixtures")
            return

    if config.upd_cont == 1:
        print("Updating contacts")
        try:
            await add_contacts.add_contacts()
            print("Updated succesfully!\n")
        except:
            print("Error. Please, check fixtures")
            return
    await log("bot", "Started", "None")
    print("Bot started succesfully!")

if __name__ == "__main__":
    from handlers import calc_fuel, commands, add_time, contacts, reports, registration
    calc_fuel.register_handlers_calc_fuel(dp)
    commands.register_handlers_commands(dp)
    add_time.register_handlers_add_time(dp)
    contacts.register_handlers_contacts(dp)
    reports.register_handlers_reports(dp)
    registration.register_handlers_registration(dp)
    executor.start_polling(dp, on_startup=on_startup)
