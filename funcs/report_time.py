import db_api


async def calc(id, month):
    timetable = await db_api.sel_time(id)
    data = {'timetable': []}
    total = 0
    for note in timetable:
        if note["start"].month == month:
            date = f'{note["start"].day}.{note["start"].month}.{note["start"].year}'
            interval = f'{note["start"].strftime("%H:%M")} - {note["end"].strftime("%H:%M")}'
            total += note["total"]
            data["timetable"].append({'date': date, 'interval': interval})
    data["total"] = f"{total:.2f}"
    return data


async def generate_msg(id, month):
    data = await calc(id, month)
    message = ''
    for note in data['timetable']:
        message += f'{note["date"]}: {note["interval"]}\n'
    message += f'\nЗа месяц вы отработали {data["total"]} часов!'
    return message
