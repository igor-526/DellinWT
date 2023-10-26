import db_api


async def calc(user_id, datefordel):
    timetable = await db_api.sel_time(user_id)
    datestripped = datefordel.split(".")
    res = {'msg': 'К удалению следующие записи: ', 'ids': []}
    for note in timetable:
        if (int(note["start"].day) ==
                int(datestripped[0]) and int(note["start"].month) ==
                int(datestripped[1])):
            date = (f'{note["start"].day}.'
                    f'{note["start"].month}.'
                    f'{note["start"].year}')
            interval = (f'{note["start"].strftime("%H:%M")} - '
                        f'{note["end"].strftime("%H:%M")}')
            res["msg"] += f'\n{date}: {interval}'
            res["ids"].append(note["id"])
    res["msg"] += '\nПодтвердить?'
    return res
