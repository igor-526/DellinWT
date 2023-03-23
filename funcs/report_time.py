import db_api
import datetime
from pprint import pprint

async def calc(id):
    timetable = await db_api.sel_time(id)
    data = {'timetable': []}
    total = 0
    for note in timetable:
        date = f'{note["start"].day}.{note["start"].month}.{note["start"].year}'
        interval = f'{note["start"].hour}:{note["start"].minute} - {note["end"].hour}:{note["end"].minute}'
        total += note["total"]
        data["timetable"].append({'date': date, 'interval': interval})
    data["total"] = total
    return data


async def generate_msg(id):
    data = await calc(id)
    message = ''
    for note in data['timetable']:
        message += f'{note["date"]}: {note["interval"]}\n'
    message += f'\nЗа месяц вы отработали {data["total"]} часов!'
    return message
