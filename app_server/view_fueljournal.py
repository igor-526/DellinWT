from flask import jsonify
from sqlalchemy import extract
import config
from models import db, Fuel


async def get_journal_fuel(year: int, month: int):
    await db.set_bind(config.POSTGRES_URI)
    query = await (Fuel.query.where(extract('month', Fuel.date) == month)
                   .where(extract('year', Fuel.date) == year).gino.all())
    db.pop_bind()
    result = {"count": len(query),
              "total_km": 0,
              "total_fuel": 0,
              "items": []}
    for note in query:
        result["total_km"] += note.milleage
        result["total_fuel"] += round(note.fuel_delta, 2)
        result["items"].append({
            "id": note.id,
            "date": int(note.date.day),
            "km": note.milleage,
            "fuel": round(note.fuel_delta, 2)
        })
    return jsonify(result)


def view_fueljournal_rules(app):
    app.add_url_rule("/journal/fuel/<int:year>/<int:month>", view_func=get_journal_fuel)
