import db_api
from pprint import pprint

async def calc(id, datefordel):
    timetable = await db_api.sel_time(id)
    datestripped = datefordel.split(".")
    res = {'msg': 'К удалению следующие записи: ', 'ids': []}
    for note in timetable:
        if int(note["start"].day) == int(datestripped[0]) and int(note["start"].month) == int(datestripped[1]):
            date = f'{note["start"].day}.{note["start"].month}.{note["start"].year}'
            interval = f'{note["start"].strftime("%H:%M")} - {note["end"].strftime("%H:%M")}'
            res["msg"] += f'\n{date}: {interval}'
            res["ids"].append(note["id"])
    res["msg"] += '\nПодтвердить?'
    return res
