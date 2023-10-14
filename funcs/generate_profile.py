import db_api

async def gen_profile(id):
    user = await db_api.sel_user(id)
    msg = f'ID: {id}\n' \
          f'Имя: {user["name"]}\n' \
          f'Город: {user["city"]}\n' \
          f'ОСП: {user["base"]}\n' \
          f'Количество рабочих дней: {user["workdays"]} ({user["workdays"]*8} часов)\n'
    if user['mode'] == 2:
        msg += "Режим: ручное управление нормой рабочих часов"
    elif user['mode'] == 1:
        msg += "Режим: автоматическое управление нормой рабочих часов (пятидневная рабочая неделя)"
    return msg