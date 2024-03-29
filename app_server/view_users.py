from flask import jsonify, request
from sqlalchemy import extract

import config
from auth import authorizate
from models import db, User, Time, City, Base
from datetime import date


async def get_user():
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await User.query.where(User.id == user['id']).gino.first()
        time = await (Time.query.where(Time.driver == user["id"]).where(
            extract('month', Time.start) == date.today().month).where(
            extract('year', Time.start) == date.today().year).gino.all())
        city = await City.query.where(City.id == user["city"]).gino.first()
        base = await Base.query.where(Base.id == user["base"]).gino.first()
    hours_worked = 0
    for note in time:
        hours_worked += note.total
    result = {"username": query.name,
              "city": city.name,
              "base": base.name,
              "mode": query.mode,
              "hours_all": query.workdays * 8,
              "hours_worked": int(hours_worked),
              "last_km": query.last_km if query.last_km else 0,
              "last_fuel": query.last_fuel if query.last_fuel else 0,
              "id": query.id,
              }

    return jsonify(result)


def view_users_rules(app):
    app.add_url_rule("/user", view_func=get_user)
