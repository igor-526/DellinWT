from models import db
from models import User, Time, Auto


async def add_user(
    number: int,
    worktime: int
):

    try:
        user = User(number=number, worktime=worktime)
        await user.create()
    except:
        print('Пользователь не добавлен')