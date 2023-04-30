import db_api
from funcs import get_wdays
from datetime import date

async def percentage(cash, total):
    perc = 0
    if cash < 1000:
        perc = 30
    elif 1000<=cash<3000:
        perc = 40
    elif 3000<=cash<6000:
        perc = 60
    elif 6000<=cash<9000:
        perc = 80
    elif 9000<=cash<12000:
        perc = 100
    elif 12000<=cash<15000:
        perc = 120
    elif cash>15000:
        perc = 150
    return {'perc': perc, 'cash': total/100*perc}


async def getworkdays(id, month, total):
    user = await db_api.sel_user(id)
    mode = user['mode']
    days = await get_wdays(month, date.today().year)
    days_plan = days['work']
    days_fact = 0
    trips = await db_api.sel_time(id)
    for note in trips:
        if note['start'].month == month:
            days_fact += 1
    res = {}
    # if days_fact:
    #     res['fact_bonus'] = await percentage(total/days_fact, total)
    # if user['mode'] == 1:
    #     res['plan_bonus'] = await percentage(total/days_plan, total)
    return res



async def gen_turnover(id, month):
    turnover = await db_api.sel_turnover(id)
    msg = 'Оборот за месяц\n'
    total = 0
    for note in turnover:
        if note.date.month == month:
            msg += f'{note.date.strftime("%d.%m")}: {note.cash} р.\n'
            total += note.cash
    msg += f'\nВсего за месяц: {total} р.\n'
    days = await getworkdays(id, month, total)
    try:
        msg += f'На данный момент ваша премия составляет {days["plan_bonus"]["perc"]}% ({days["plan_bonus"]["cash"]} р.)\n'
    except: pass
    try:
        msg += f'По кол-ву добавленных раб. дней ваша премия составляет {days["fact_bonus"]["perc"]}% ({days["fact_bonus"]["cash"]} р.)'
    except: pass
    return msg
