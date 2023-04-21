import db_api

async def calc(id, month):
    fueltable = await db_api.sel_fuel(id)
    data = {'fueltable': []}
    total_m = 0
    total_f = 0
    total_fb = 0
    total_fe = 0
    msg = 'Поездки за месяц:\n'
    for note in fueltable:
        if note["date"].month == month:
            msg += f'{note["date"].strftime("%d.%m")}: {note["milleage"]} км; {note["fuel_delta"]} л.\n'
            total_m += note['milleage']
            total_f += note["fuel_delta"]
    data["total_m"] = f"{total_m:.2f}"
    data["total_f"] = f"{total_f:.2f}"
    msg += f'\nЗа месяц вы проехали: {total_m:.2f}\n' \
           f'Топливо по норме: {total_f:.2f}'
    return msg


async def fordel(id, datefordel):
    fueltable = await db_api.sel_fuel(id)
    datestripped = datefordel.split(".")
    res = {'msg': 'К удалению следующие записи: \n', 'ids': []}
    for note in fueltable:
        if int(note['date'].month) == int(datestripped[1]) and int(note['date'].day) == int(datestripped[0]):
            res['msg'] += f'{note["date"].strftime("%d.%m")}: {note["milleage"]} км; {note["fuel_delta"]} л.\n'
            res['ids'].append(int(note['id']))
    res["msg"] += '\nПодтвердить?'
    return res
