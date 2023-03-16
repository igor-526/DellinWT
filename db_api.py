from models import db, User, Time, Auto


async def add_user(
    id: int,
    number: int,
    worktime: int):
    user = User(id=id, number=number, worktime=worktime)
    await user.create()


async def chk_user(id):
    user = await db.scalar(db.exists().where(User.id == id).select())
    return user


async def add_auto(name: str,
                   consumption: float,
                   tank: int):
    try:
        auto = Auto(name=name, consumption=consumption, tank=tank)
        await auto.create()
    except:
        print('Автомобиль не добавлен')


async def show_auto():
    auto = await Auto.query.gino.all()
    auto_list = []
    for i in auto:
        auto_list.append({'id': i.id, 'name': i.name, 'consumption': i.consumption, 'tank': i.tank})
    return auto_list


async def sel_auto(name: str):
    auto = await Auto.query.where(Auto.name == name).gino.first()
    info = {}
    info['consumption'] = auto.consumption
    info['tank'] = auto.tank
    return info