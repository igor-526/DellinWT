import db_api
from datetime import date


async def calc(user_id, month):
    timetable = await db_api.sel_time(user_id)
    usr = await db_api.sel_user(user_id)
    data = {'timetable': [], 'delta': None}
    total = 0
    for note in timetable:
        if note["start"].month == month and note["start"].year == date.today().year:
            date = (f'{note["start"].day}.'
                    f'{note["start"].month}.'
                    f'{note["start"].year}')
            interval = (f'{note["start"].strftime("%H:%M")} - '
                        f'{note["end"].strftime("%H:%M")}')
            total += note["total"]
            data["timetable"].append({'date': date,
                                      'interval': interval})
    data["total"] = f"{total:.2f}"
    data['delta'] = usr['workdays'] * 8 - total
    return data


async def generate_msg(user_id, month):
    data = await calc(user_id, month)
    message = ''
    for note in data['timetable']:
        message += f'{note["date"]}: {note["interval"]}\n'
    message += f'\nЗа месяц вы отработали {data["total"]} часов!\n'
    if data['delta'] > 0:
        message += f'До нормы не хватает {data["delta"]:.2f} часов!'
    elif data['delta'] < 0:
        message += f'Переработка составляет {data["delta"]*(-1):.2f} часов!'
    return message
