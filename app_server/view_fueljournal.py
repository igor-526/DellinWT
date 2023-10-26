from flask import jsonify, request
from auth import authorizate
from sqlalchemy import extract
import config
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
            return jsonify({"status": "OK"})
        else:
            return jsonify({"status": "no permission"})


def view_fueljournal_rules(app):
    app.add_url_rule("/journal/fuel/<int:year>/<int:month>",
                     view_func=get_journal_fuel)
    app.add_url_rule("/journal/fuel/<int:note_id>",
                     view_func=delete_fuel_note, methods=["DELETE"])
