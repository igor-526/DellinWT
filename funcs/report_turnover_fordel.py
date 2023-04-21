import db_api

async def calc(id, datefordel):
    turnover = await db_api.sel_turnover(id)
    datestripped = datefordel.split(".")
    res = {'msg': 'К удалению следующие записи: \n', 'ids': []}
    for note in turnover:
        if int(note.date.day) == int(datestripped[0]) and int(note.date.month) == int(datestripped[1]):
            res['msg'] += f'{note.date.strftime("%d.%m")}: {note.cash}\n'
            res['ids'].append(note.id)
    res["msg"] += '\nПодтвердить?'
    return res
