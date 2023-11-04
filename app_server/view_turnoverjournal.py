from flask import jsonify, request
from auth import authorizate
from sqlalchemy import extract
import config
import db_api
import datetime
from models import db, Turnover


async def get_journal_turnover(year: int, month: int):
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await (Turnover.query.where(Turnover.driver == user["id"])
                       .where(extract('month', Turnover.date) == month)
                       .where(extract('year', Turnover.date) == year)
                       .gino.all())
    result = {"count": len(query),
              "total": 0,
              "items": []}
    for note in query:
        result["total"] += round(note.cash, 2)
        result["items"].append({
            "id": note.id,
            "date": str(note.date),
            "cash": round(note.cash, 2)
        })
    return jsonify(result)


async def delete_turnover_note(note_id: int):
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await Turnover.query.where(Turnover.id == note_id).gino.first()
        if not query:
            return jsonify({"status": "not found"})
        if query.driver == user['id']:
            await query.delete()
            return jsonify({"status": "OK"})
        else:
            return jsonify({"status": "no permission"})


async def add_turnover_note():
    user = await authorizate(request.headers.get("Authorization"))
    date = datetime.datetime.strptime(request.headers.get("date"), '%Y-%m-%d').date()
    async with db.with_bind(config.POSTGRES_URI):
        await db_api.add_turnover(driver=user['id'],
                                  cash=float(request.headers.get("cash")),
                                  date=date)
    return jsonify({"status": "ok"})


async def change_turnover_note(note_id):
    user = await authorizate(request.headers.get("Authorization"))
    date = datetime.datetime.strptime(request.headers.get("date"), '%Y-%m-%d').date()
    async with db.with_bind(config.POSTGRES_URI):
        query = await Turnover.query.where(Turnover.id == note_id)
        if query.driver == user['id']:
            await query.update(date=date,
                               cash=float(request.headers.get("cash"))).apply()
        else:
            return jsonify({"status": "no permission"})


def view_turnoverjournal_rules(app):
    app.add_url_rule("/journal/turnover/<int:year>/<int:month>",
                     view_func=get_journal_turnover)
    app.add_url_rule("/journal/turnover/<int:note_id>",
                     view_func=delete_turnover_note, methods=["DELETE"])
    app.add_url_rule("/journal/turnover",
                     view_func=add_turnover_note, methods=["POST"])
    app.add_url_rule("/journal/turnover/<int:note_id>")
