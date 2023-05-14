import jwt
from flask import Blueprint, current_app, json, jsonify, request
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import mongo

auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()


@auth.route("/signup", methods=["POST"])
def signup():
    data = json.loads(request.data)
    username = data["username"]
    password = data["password"]
    existing_user = mongo["users"].find_one({"username": username})
    if existing_user:
        return json.dumps({"error": "User already exists"}), 400
    else:
        mongo["users"].insert_one(
            {"username": username, "password": generate_password_hash(password)}
        )
        return jsonify(
            {
                "id": mongo["users"]
                .find_one({"username": data["username"]})["_id"]
                .__str__()
            }
        )


@auth.route("/login", methods=["POST"])
def login_user():
    try:
        data = json.loads(request.data)
        username = data["username"]
        password = data["password"]
    except:
        return jsonify({"message": "Incomplete credentials provided"}), 401

    user = mongo["users"].find_one({"username": username})
    if user is None:
        return jsonify({"message": "Invalid credentials provided"}), 401

    if check_password_hash(user["password"], password):
        token = jwt.encode(
            {
                "user_id": str(user["_id"]),
            },
            current_app.config["SECRET_KEY"],
            "HS256",
        )

        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials provided"}), 401
