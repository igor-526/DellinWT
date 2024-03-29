from flask import jsonify, request
from auth import authorizate
from sqlalchemy import extract
import config
import datetime
import db_api
from models import db, Fuel


async def get_journal_fuel(year: int, month: int):
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await (Fuel.query.where(Fuel.driver == user["id"])
                       .where(extract('month', Fuel.date) == month)
                       .where(extract('year', Fuel.date) == year).gino.all())
    result = {"count": len(query),
              "total_km": 0,
              "total_fuel": 0,
              "items": []}
    for note in query:
        result["total_km"] += note.milleage
        result["total_fuel"] += round(note.fuel_delta, 2)
        result["items"].append({
            "id": note.id,
            "date": str(note.date),
            "km": note.milleage,
            "fuel": round(note.fuel_delta, 2)
        })
    return jsonify(result)


async def delete_fuel_note(note_id: int):
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await Fuel.query.where(Fuel.id == note_id).gino.first()
        if not query:
            return jsonify({"status": "not found"})
        if query.driver == user['id']:
            await query.delete()
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "no permission"})


async def add_fuel_note():
    user = await authorizate(request.headers.get("Authorization"))
    date = datetime.datetime.strptime(request.headers.get("date"), '%Y-%m-%d').date()
    try:
        async with db.with_bind(config.POSTGRES_URI):
            new = await db_api.add_fuel(driver=user['id'],
                                        milleage=int(request.headers.get('milleage')),
                                        fuel_delta=float(request.headers.get('fuel_delta')),
                                        date=date,
                                        f_odo=int(request.headers.get('f_odo')),
                                        f_fuel=float(request.headers.get('f_fuel')),
                                        s_odo=int(request.headers.get('s_odo')),
                                        s_fuel=float(request.headers.get('s_fuel')),
                                        auto=int(request.headers.get('auto')),
                                        econ_fuel=float(request.headers.get('econ_fuel')),
                                        over_fuel=float(request.headers.get('over_fuel')))
        return jsonify({"status": new})
    except Exception:
        return jsonify({"status": "error"})


async def change_fuel_note(note_id: int):
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await Fuel.query.where(Fuel.id == note_id).gino.first()
        if query.driver == user['id']:
            date = datetime.datetime.strptime(request.headers.get("date"), '%Y-%m-%d').date()
            await query.update(driver=user['id'],
                               milleage=int(request.headers.get('milleage')),
                               fuel_delta=float(request.headers.get('fuel_delta')),
                               date=date,
                               f_odo=int(request.headers.get('f_odo')),
                               f_fuel=float(request.headers.get('f_fuel')),
                               s_odo=int(request.headers.get('s_odo')),
                               s_fuel=float(request.headers.get('s_fuel')),
                               auto=int(request.headers.get('auto')),
                               econ_fuel=float(request.headers.get('econ_fuel')),
                               over_fuel=float(request.headers.get('over_fuel'))).apply()
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "no permission"})


async def get_auto():
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        autos = await db_api.show_auto(user['city'])
    return jsonify(autos)


def view_fueljournal_rules(app):
    app.add_url_rule("/journal/fuel/<int:year>/<int:month>",
                     view_func=get_journal_fuel)
    app.add_url_rule("/journal/fuel/<int:note_id>",
                     view_func=delete_fuel_note, methods=["DELETE"])
    app.add_url_rule("/journal/fuel",
                     view_func=add_fuel_note, methods=["POST"])
    app.add_url_rule("/journal/fuel/<int:note_id>",
                     view_func=change_fuel_note, methods=['PATCH'])
    app.add_url_rule("/journal/auto",
                     view_func=get_auto)
