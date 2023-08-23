from aiogram.utils import executor
import schedule_tasks
import config
from funcs import add_auto, add_contacts, add_city, add_base, log
from models import db_bind, db_reset
from create_bot import dp
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def on_startup(_):
    print("Connecting to database...")
    try:
        await db_bind()
        print("Connected to database succesfully!\n")
    except Exception as ex:
        print("Couldn't connect to database. Please, check")
        print(ex)
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
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(schedule_tasks.upd_wd, trigger='cron', day=1, hour=8,
                      minute=0)
    scheduler.start()
    print("Bot started succesfully!")

if __name__ == "__main__":
    from handlers import commands, add_time, contacts, reports, registration, settings, turnover, report

    from handlers import (register_handlers_cf_s_odo,
                          register_handlers_cf_f_odo,
                          register_handlers_cf_fuel,
                          register_handlers_cf_refuel,
                          register_handlers_cf_sel_auto,
                          register_handlers_cf_confirm)

    commands.register_handlers_commands(dp)

    register_handlers_cf_s_odo(dp)
    register_handlers_cf_f_odo(dp)
    register_handlers_cf_fuel(dp)
    register_handlers_cf_refuel(dp)
    register_handlers_cf_sel_auto(dp)
    register_handlers_cf_confirm(dp)

    add_time.register_handlers_add_time(dp)
    contacts.register_handlers_contacts(dp)
    reports.register_handlers_reports(dp)
    registration.register_handlers_registration(dp)
    settings.register_handlers_settings(dp)
    turnover.register_handlers_turnover(dp)
    report.register_handlers_reportissue(dp)
    executor.start_polling(dp, on_startup=on_startup)
