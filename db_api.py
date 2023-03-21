from models import db, User, Time, Auto


async def add_user(
    id: int,
    name: int,
        ):
    user = User(id=id, name=name)
    await user.create()


async def chk_user(id):
    user = await db.scalar(db.exists().where(User.id == id).select())
    return user


async def chk_reg(id):
    user = await User.query.where(User.id == id).gino.first()
    return user.worktime


async def add_wt(id: int, time: int):
    updated_user = await User.query.where(User.id == id).gino.first()
    await updated_user.update(worktime=time).apply()


async def add_auto(name: str,
                   consumption: float,
                   tank: int):
    try:
        auto = Auto(name=name, consumption=consumption, tank=tank)
        await auto.create()
    except:
        print('Автомобиль не добавлен')


async def add_time(id, date, start, end, c):
    time = Time(driver=id, date=date, start=start, end=end, c=c)
    await time.create()




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