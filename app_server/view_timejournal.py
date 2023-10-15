from flask import jsonify, request
from auth import authorizate
from sqlalchemy import extract
import config
from models import db, Time


async def get_journal_time(year: int, month: int):
    user = authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await (Time.query.where(Time.driver == user["id"]).where(extract('month', Time.start) == month)
                       .where(extract('year', Time.start) == year).gino.all())
    db.pop_bind()
    result = {"count": len(query),
              "total": 0,
              "items": []}
    for note in query:
        result["total"] += note.total
        result["items"].append({
            "id": note.id,
            "date": int(note.start.day),
            "start": str(note.start.time().strftime("%H:%M")),
            "end": str(note.end.time().strftime("%H:%M")),
            "total": round(note.total, 2),
            "c": int(note.c)
        })
    return jsonify(result)


def view_timejournal_rules(app):
    app.add_url_rule("/journal/time/<int:year>/<int:month>", view_func=get_journal_time)
