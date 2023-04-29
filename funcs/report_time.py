import db_api


async def calc(id, month):
    timetable = await db_api.sel_time(id)
    usr = await db_api.sel_user(id)
    data = {'timetable': [], 'delta': None}
    total = 0
    for note in timetable:
        if note["start"].month == month:
            date = f'{note["start"].day}.{note["start"].month}.{note["start"].year}'
            interval = f'{note["start"].strftime("%H:%M")} - {note["end"].strftime("%H:%M")}'
            total += note["total"]
            data["timetable"].append({'date': date, 'interval': interval})
    data["total"] = f"{total:.2f}"
    data['delta'] = usr['workdays']*8-total
    return data


async def generate_msg(id, month):
    data = await calc(id, month)
    message = ''
    for note in data['timetable']:
        message += f'{note["date"]}: {note["interval"]}\n'
    message += f'\nЗа месяц вы отработали {data["total"]} часов!\n'
    if data['delta'] > 0:
        message += f'До нормы не хватает {data["delta"]:.2f} часов!'
    elif data['delta'] < 0:
        message += f'Переработка составляет {data["delta"]*(-1):.2f} часов!'
    return message
