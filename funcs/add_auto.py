import db_api
import csv


async def add_auto():
    await db_api.del_autos()
    with open("fixtures/auto.csv", encoding='utf-8') as autos:
        reader = csv.reader(autos, delimiter=",")
        for auto in reader:
            await db_api.add_auto(int(auto[0]), int(auto[1]), str(auto[2]), float(auto[3]), int(auto[4]))
