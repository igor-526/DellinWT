import db_api
import csv


async def add_base():
    with open("fixtures/base.csv", encoding='utf-8') as bases:
        reader = csv.reader(bases, delimiter=",")
        for base in reader:
            await db_api.add_base(int(base[0]),
                                  int(base[1]),
                                  str(base[2]))
