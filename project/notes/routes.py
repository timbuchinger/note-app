import json

from bson import json_util
from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request

from ..auth.decorators import jwt_required
from ..extensions import mongo

notes = Blueprint("notes", __name__)


@notes.route("", methods=["GET"])
@jwt_required
def get_notes(user_id):
    notes = mongo["notes"].find(
        {
            "$or": [{"user_id": user_id}, {"shared_with": user_id}],
        }
    )
    return (
        json.loads(json_util.dumps(list(notes))),
        200,
    )


@notes.route("/<string:note_id>", methods=["GET"])
@jwt_required
def get_note(user_id, note_id):
    note = mongo["notes"].find_one(
        {
            "$and": [
                {"_id": ObjectId(note_id)},
                {"$or": [{"user_id": user_id}, {"shared_with": user_id}]},
            ]
        }
    )
    if note:
        return json.loads(json_util.dumps(note)), 200
    else:
        return jsonify({"message": "Note not found"}), 404


@notes.route("", methods=["POST"])
@jwt_required
def create_note(user_id):
    try:
        data = json.loads(request.data)
        title = data["title"]
        content = data["content"]
    except:
        return jsonify({"message": "Invalid request"}), 400

    result = mongo["notes"].insert_one(
        {"user_id": user_id, "title": title, "content": content}
    )
    return jsonify({"id": str(result.inserted_id), "message": "Note created"}), 200


@notes.route("/<string:note_id>", methods=["PUT"])
@jwt_required
def update_note(user_id, note_id):
    try:
        data = json.loads(request.data)
        title = data["title"]
        content = data["content"]
    except:
        return jsonify({"message": "Invalid request"}), 400

    result = mongo["notes"].update_one(
        {"_id": ObjectId(note_id), "user_id": user_id},
        {"$set": {"title": title, "content": content}},
    )

    if result.modified_count == 0:
        return jsonify({"message": "No updates applied, or note not found"}), 400
    else:
        return jsonify({"message": "Note updated"}), 200


@notes.route("/<string:note_id>", methods=["DELETE"])
@jwt_required
def delete_note(user_id, note_id):
    result = mongo["notes"].delete_one({"_id": ObjectId(note_id), "user_id": user_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Note not found"}), 404
    else:
        return jsonify({"message": "Note deleted"}), 200


@notes.route("/<string:note_id>/share", methods=["POST"])
@jwt_required
def share_note(user_id, note_id):
    data = json.loads(request.data)
    shared_with = data["shared_with"]
    result = mongo["notes"].update_one(
        {"_id": ObjectId(note_id), "user_id": user_id},
        {"$push": {"shared_with": shared_with}},
    )

    if result.modified_count == 0:
        return jsonify({"message": "Note not found"}), 404
    else:
        return jsonify({"message": "Note shared"}), 200
