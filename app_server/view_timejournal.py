from flask import jsonify, request
from auth import authorizate
from sqlalchemy import extract
import config
from models import db, Time


async def get_journal_time(year: int, month: int):
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await (Time.query.where(Time.driver == user["id"])
                       .where(extract('month', Time.start) == month)
                       .where(extract('year', Time.start) == year).gino.all())
    result = {"count": len(query),
              "total": 0,
              "items": []}
    for note in query:
        result["total"] += note.total
        result["items"].append({
            "id": note.id,
            "start": str(note.start),
            "end": str(note.end),
            "total": round(note.total, 2),
            "c": int(note.c)
        })
    return jsonify(result)


async def delete_time_note(note_id: int):
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await Time.query.where(Time.id == note_id).gino.first()
        if not query:
            return jsonify({"status": "not found"})
        if query.driver == user['id']:
            await query.delete()
            return jsonify({"status": "OK"})
        else:
            return jsonify({"status": "no permission"})


def view_timejournal_rules(app):
    app.add_url_rule("/journal/time/<int:year>/<int:month>",
                     view_func=get_journal_time)
    app.add_url_rule("/journal/time/<int:note_id>",
                     view_func=delete_time_note, methods=["DELETE"])
