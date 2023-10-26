import requests


async def get_wdays(month: int, year: int):
    url = f'https://isdayoff.ru/api/getdata?year={year}&month={month}'
    response = requests.get(url)
    work = 0
    not_work = 0
    for day in response.text:
        if day == "1":
            not_work += 1
        elif day == "0":
            work += 1
    hours = work * 8
    return {"work": work, "not_work": not_work, "hours": hours}
