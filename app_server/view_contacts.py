from flask import jsonify, request
from auth import authorizate
import config
from models import db, Contacts


def get_result(query):
    result = {"count": len(query), "items": []}
    for contact in query:
        result["items"].append({
            "name": f'{contact.last_name} '
                    f'{contact.first_name} '
                    f'{contact.middle_name}',
            "position": contact.position,
            "comment": contact.comment,
            "phone": contact.phone
        })
    return jsonify(result)


async def get_contacts():
    user = await authorizate(request.headers.get("Authorization"))
    async with db.with_bind(config.POSTGRES_URI):
        query = await Contacts.query.where(
            Contacts.city == user["city"]).order_by('last_name').gino.all()
    return get_result(query)


def view_contacts_rules(app):
    app.add_url_rule("/contacts/",
                     view_func=get_contacts)
