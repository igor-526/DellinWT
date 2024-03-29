import string
from datetime import date
from flask import jsonify, request
from models import db, User, Tokens
import random
import config
from create_bot import bot


async def authorizate(token: str):
    async with db.with_bind(config.POSTGRES_URI):
        token_note = await Tokens.query.where(
            Tokens.token == token).gino.first()
        if token_note:
            user = await User.query.where(
                User.id == token_note.driver).gino.first()
            return {"id": user.id,
                    "city": user.city,
                    "base": user.base}


async def send_code():
    user_id = request.headers.get("user_id")
    if not user_id:
        return jsonify({"status": "no_header"})
    try:
        int(user_id)
    except Exception:
        return jsonify({"status": "error"})
    async with db.with_bind(config.POSTGRES_URI):
        user = await User.query.where(User.id == int(user_id)).gino.first()
        if not user:
            return jsonify({"status": "not found"})
        else:
            c = random.randint(100000, 999999)
            code = await Tokens.query.where(
                Tokens.driver == int(user_id)).gino.first()
            if code:
                await code.update(code=c).apply()
            else:
                code = Tokens(driver=int(user_id),
                              code=c,
                              last_used=date.today())
                await code.create()
            await bot.send_message(chat_id=user_id,
                                   text=str(c))
            return jsonify({"status": user.name})


async def send_token(user_id: int):
    code = request.headers.get("code")
    async with db.with_bind(config.POSTGRES_URI):
        token_note = await Tokens.query.where(
            Tokens.driver == user_id).gino.first()
        token = ''.join(random.choice(string.ascii_letters) for i in range(10))
        if not token_note:
            return jsonify({"status": "no user"})
        else:
            try:
                int(code)
            except Exception:
                return jsonify({"status": "error"})
            if token_note.code == int(code):
                token_note.token = token
                await token_note.update(token=token, code=None).apply()
                return jsonify({"status": token})
            else:
                return jsonify({"status": "missmatching"})


async def chk_token():
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        return jsonify({"status": "False"})
    else:
        async with db.with_bind(config.POSTGRES_URI):
            token_note = await Tokens.query.where(
                Tokens.token == auth_token).gino.first()
            if token_note:
                return jsonify({"status": "True"})
            else:
                return jsonify({"status": "False"})


def view_auth_rules(app):
    app.add_url_rule("/auth",
                     view_func=send_code, methods=['POST'])
    app.add_url_rule("/auth/<int:user_id>",
                     view_func=send_token, methods=["GET"])
    app.add_url_rule("/auth/check",
                     view_func=chk_token, methods=['GET'])
