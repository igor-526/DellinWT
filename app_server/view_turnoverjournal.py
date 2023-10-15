from flask import jsonify, request
from auth import authorizate
from sqlalchemy import extract
import config
from models import db, Turnover


async def get_journal_turnover(year: int, month: int):
    user = authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await (Turnover.query.where(Turnover.driver == user["id"]).where(extract('month', Turnover.date) == month)
                       .where(extract('year', Turnover.date) == year).gino.all())
    db.pop_bind()
    result = {"count": len(query),
              "total": 0,
              "items": []}
    for note in query:
        result["total"] += round(note.cash, 2)
        result["items"].append({
            "id": note.id,
            "date": int(note.date.day),
            "cash": round(note.cash, 2)
        })
    return jsonify(result)


def view_turnoverjournal_rules(app):
    app.add_url_rule("/journal/turnover/<int:year>/<int:month>", view_func=get_journal_turnover)
