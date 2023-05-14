from functools import wraps

import jwt
from flask import current_app, jsonify, request


def jwt_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({"message": "A token must be provided"}), 400
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            user_id = data["user_id"]
        except:
            return jsonify({"message": "The provided token is invalid"}), 400

        return f(user_id, *args, **kwargs)

    return decorator
