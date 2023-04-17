import db_api
import csv


async def add_city():
    with open("fixtures/city.csv", encoding='utf-8') as cities:
        reader = csv.reader(cities, delimiter=",")
        for city in reader:
            await db_api.add_city(int(city[0]), str(city[1]))
