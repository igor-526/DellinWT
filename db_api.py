from models import db, User, Time, Auto, Contacts, City, Base, Fuel, Turnover
from funcs import get_wdays
from datetime import date


async def add_user(id: int,
                   name: int,
                   city: int,
                   base: int,
                   mode: int,
                   workdays: int):
    user = User(id=id, name=name, city=city, base=base, mode=mode, workdays=workdays)
    await user.create()


async def add_auto(city: int,
                   name: str,
                   consumption: float,
                   tank: int):
    try:
        auto = Auto(name=name, consumption=consumption, tank=tank, city=city)
        await auto.create()
    except:
        pass


async def add_time(id, start, end, c, total):
    time = Time(driver=id, start=start, end=end, c=c, total=total)
    await time.create()


async def add_wt(id: int, time: int):
    updated_user = await User.query.where(User.id == id).gino.first()
    await updated_user.update(worktime=time).apply()


async def add_contact(city: int,
                      position: str,
                      last_name: str,
                      first_name: str,
                      middle_name: str,
                      comment: str,
                      phone: str):
    try:
        contact = Contacts(position=position,
                           first_name=first_name,
                           last_name=last_name,
                           middle_name=middle_name,
                           comment=comment,
                           phone=phone,
                           city=city)
        await contact.create()
    except Exception as ex:
        pass


async def add_city(id: int, name: str):
    try:
        city = City(id=id, name=name)
        await city.create()
    except:
        pass


async def add_base(id: int, city:int, name: str):
    try:
        base = Base(id = id, city = city, name = name)
        await base.create()
    except:
        pass


async def add_fuel(id: int,
                   milleage: int,
                   fuel_delta: float,
                   date,
                   f_odo,
                   f_fuel):

    fuel = Fuel(driver=id, milleage=milleage, fuel_delta=fuel_delta, date=date)
    user = await User.query.where(User.id == id).gino.first()
    await user.update(last_km=f_odo, last_fuel=f_fuel).apply()
    await fuel.create()
    return True


async def add_turnover(driver, cash, date):
    turnover = Turnover(driver=driver, cash=cash, date=date)
    await turnover.create()


async def chk_user(id):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def show_auto(city=1):
    auto = await Auto.query.where(Auto.city == city).gino.all()
    auto_list = []
    for i in auto:
        auto_list.append({'id': i.id, 'name': i.name, 'consumption': i.consumption, 'tank': i.tank})
    return auto_list


async def show_contacts(position=None, city=1):
    contacts = await Contacts.query.where(Contacts.city == city).order_by('last_name').gino.all()
    result = []
    for contact in contacts:
        if contact.position:
            if contact.position == position:
                result.append(contact)
        else:
            return contacts
    return result


async def show_cities():
    cities = await City.query.gino.all()
    return cities


async def show_bases(city: int):
    bases = await Base.query.where(Base.city == city).gino.all()
    return bases


async def city_id(city):
    city = await City.query.where(City.name == city).gino.first()
    return city.id


async def base_id(base):
    base = await Base.query.where(Base.name == base).gino.first()
    return base.id


async def search_contacts(q):
    qq = q.split(' ')
    result = []
    for item in qq:
        r_ln = await Contacts.query.where(Contacts.last_name == item).gino.all()
        r_fn = await Contacts.query.where(Contacts.first_name == item).gino.all()
        r_mn = await Contacts.query.where(Contacts.middle_name == item).gino.all()
        for r in r_ln:
            if r not in result:
                result.append(r)
        for r in r_fn:
            if r not in result:
                result.append(r)
        for r in r_mn:
            if r not in result:
                result.append(r)
    return result


async def sel_auto(name: str):
    auto = await Auto.query.where(Auto.name == name).gino.first()
    info = {}
    info['consumption'] = auto.consumption
    info['tank'] = auto.tank
    return info


async def sel_time(id):
    timetable = await Time.query.where(Time.driver == id).gino.all()
    info = []
    for time in timetable:
        info.append({"start": time.start, "end": time.end, "total": time.total, "id": time.id})
    return info


async def sel_fuel(id):
    fueltable = await Fuel.query.where(Fuel.driver == id).gino.all()
    info = []
    for note in fueltable:
        info.append({"milleage": note.milleage, "fuel_delta": note.fuel_delta,
                     "date": note.date, 'id': note.id})
    return info


async def sel_user(id):
    user = await User.query.where(User.id == id).gino.first()
    city = await City.query.where(City.id == user.city).gino.first()
    base = await Base.query.where(Base.id == user.base).gino.first()
    data = {'name': user.name, 'city': city.name, 'base': base.name, 'mode': user.mode, 'workdays': user.workdays}
    return data


async def sel_all_users():
    users = await User.query.gino.all()
    ids = []
    for user in users:
        ids.append(user.id)
    return ids


async def del_time(ids):
    for id in ids:
        note = await Time.query.where(Time.id == id).gino.first()
        await note.delete()


async def del_turnover(ids):
    for id in ids:
        note = await Turnover.query.where(Turnover.id == id).gino.first()
        await note.delete()


async def del_fuel(ids):
    for id in ids:
        note = await Fuel.query.where(Fuel.id == id).gino.first()
        await note.delete()


async def del_user(id):
    time = await Time.query.where(Time.driver == id).gino.all()
    fuel = await Fuel.query.where(Fuel.driver == id).gino.all()
    turnover = await Turnover.query.where(Turnover.driver == id).gino.all()
    user = await User.query.where(User.id == id).gino.first()
    for note in time:
        await note.delete()
    for note in fuel:
        await note.delete()
    for note in turnover:
        await note.delete()
    await user.delete()


async def upd_user(id: int,
                   name=None,
                   city=None,
                   base=None,
                   mode=None,
                   workdays=None):
    user = await User.query.where(User.id == id).gino.first()
    if name:
        await user.update(name=name).apply()
    if city and base:
        await user.update(city=city, base=base).apply()
    if mode:
        await user.update(mode=mode).apply()
    if workdays:
        await user.update(workdays=workdays).apply()

async def sel_turnover(id):
    turnover = await Turnover.query.where(Turnover.driver == id).gino.all()
    return turnover


async def update_wdays():
    fulltimers = await User.query.where(User.mode == 1).gino.all()
    freetimers = await User.query.where(User.mode == 2).gino.all()
    new_wd = await get_wdays(date.today().month, date.today().year)
    full_ids = []
    free_ids = []
    for usr in fulltimers:
        await usr.update(workdays=new_wd['work']).apply()
        full_ids.append(usr.id)
    for usr in freetimers:
        await usr.update(workdays=0).apply()
        free_ids.append(usr.id)
    return {'full_ids': full_ids, 'free_ids': free_ids, 'new_wd': new_wd}


async def del_contacts():
    cont = await Contacts.query.gino.all()
    for contact in cont:
        await contact.delete()


async def del_autos():
    autos = await Auto.query.gino.all()
    for auto in autos:
        await auto.delete()
