import db_api


async def calc(id, month):
    fueltable = await db_api.sel_fuel(id)
    data = {'fueltable': []}
    total_m = 0
    total_f = 0
    total_fb = 0
    total_fe = 0
    for note in fueltable:
        if note["date"].month == month:
            data['fueltable'].append({"date": note['date'], "milleage": note['milleage'], "fuel_delta": note["fuel_delta"]})
            total_m += note['milleage']
            total_f += note["fuel_delta"]
            total_fb += note["fuel_burnout"]
            total_fe += note["fuel_economy"]
    data["total_m"] = f"{total_m:.2f}"
    data["total_f"] = f"{total_f:.2f}"
    data["total_fb"] = f"{total_fb:.2f}"
    data["total_fe"] = f"{total_fe:.2f}"
    return data


async def generate_msg(id, month):
    data = await calc(id, month)
    message = ''
    for note in data['fueltable']:
        message += f'{note["date"]}: {note["milleage"]}км, {note["fuel_delta"]} л.\n'
    message += f'\nЗа месяц вы проехали: {data["total_m"]}'
    message += f'\nТопливо по норме: {data["total_f"]}'
    message += f'\nПережоги по ПЛ: {data["total_fb"]}'
    message += f'\nЭкономия по ПЛ: {data["total_fe"]}'
    return message
