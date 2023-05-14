import json

from bson import json_util
from flask import Blueprint, jsonify, request

from ..auth.decorators import jwt_required
from ..extensions import mongo

note_search = Blueprint("note_search", __name__)


@note_search.route("", methods=["GET"])
@jwt_required
def search(user_id):
    q = request.args.get("q")
    result = list(
        mongo["notes"].find(
            {
                "$and": [
                    {"$text": {"$search": q}},
                    {"$or": [{"user_id": user_id}, {"shared_with": user_id}]},
                ]
            }
        )
    )
    if len(result) == 0:
        return jsonify({"message": "No notes found"}), 404
    else:
        return json.loads(json_util.dumps(result))
