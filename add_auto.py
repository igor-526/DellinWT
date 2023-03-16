import db_api

async def add_auto():
    with open('auto.txt', 'r') as file:
        for line in file.readlines():
            auto = line.strip('\n').split(' | ')
            await db_api.add_auto(str(auto[0]), float(auto[1]), int(auto[2]))