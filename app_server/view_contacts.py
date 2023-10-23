from flask import jsonify, request
from auth import authorizate
import config
from models import db, Contacts


def get_result(query):
    result = {"count": len(query), "items": []}
    for contact in query:
        result["items"].append({
            "name": f'{contact.last_name} {contact.first_name} {contact.middle_name}',
            "position": contact.position,
            "comment": contact.comment,
            "phone": contact.phone
        })
    return jsonify(result)


async def get_contacts():
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await Contacts.query.where(Contacts.city == user["city"]).order_by('last_name').gino.all()
    db.pop_bind()
    return get_result(query)


async def get_contacts_position(position: str):
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await (Contacts.query.where(Contacts.city == user["city"]).where(Contacts.position == position.capitalize())
                       .order_by('last_name').gino.all())
    db.pop_bind()
    return get_result(query)


async def get_positions():
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await (Contacts.query.where(Contacts.city == user["city"]).gino.all())
    db.pop_bind()
    positions = []
    for contact in query:
        if contact.position not in positions:
            positions.append(contact.position)
    return jsonify(positions)


def view_contacts_rules(app):
    app.add_url_rule("/contacts/positions", view_func=get_positions)
    app.add_url_rule("/contacts/<position>/", view_func=get_contacts_position)
    app.add_url_rule("/contacts/", view_func=get_contacts)
