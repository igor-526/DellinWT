import db_api
import csv


async def add_auto():
    with open("fixtures/auto.csv", encoding='utf-8') as autos:
        reader = csv.reader(autos, delimiter = ",")
        for auto in reader:
            await db_api.add_auto(int(auto[0]), str(auto[1]), float(auto[2]), int(auto[3]))