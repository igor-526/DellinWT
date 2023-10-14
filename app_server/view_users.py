from flask import jsonify
import config
from models import db, User


async def get_user(user_id: int):
    await db.set_bind(config.POSTGRES_URI)
    query = await (User.query.where(User.id == user_id).gino.first())
    db.pop_bind()
    result = {"username": query.name,
              "city": str(query.city),
              "base": str(query.base),
              "mode": str(query.mode),
              "hours_all": query.workdays * 8,
              "last_km": query.last_km,
              "last_fuel": query.last_fuel,
              "id": query.id,
              }
    return jsonify(result)


def view_users_rules(app):
    app.add_url_rule("/users/<int:user_id>", view_func=get_user)
