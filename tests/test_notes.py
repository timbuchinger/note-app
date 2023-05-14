import json

from tests.conftest import load_sample_notes


def test_note_create_and_then_get(client, login):
    client.post(
        "/api/notes",
        data=json.dumps({"title": "Test Title", "content": "Note content."}),
        headers={"x-access-tokens": login},
    )
    client.post(
        "/api/notes",
        data=json.dumps({"title": "Test Title 2", "content": "Note content 2."}),
        headers={"x-access-tokens": login},
    )

    response = client.get(
        "/api/notes",
        headers={"x-access-tokens": login},
    )

    assert len(response.json) == 2
    assert response.status_code == 200


def test_note_create_invalid_content(client, login):
    response = client.post(
        "/api/notes",
        data=json.dumps({"title": "Test Title"}),
        headers={"x-access-tokens": login},
    )
    assert response.status_code == 400
    assert response.json["message"] == "Invalid request"


def test_note_get_single(client, login):
    load_sample_notes(client, login)

    response = client.get(
        "/api/notes",
        headers={"x-access-tokens": login},
    )

    assert response.json[0]["title"] == "1st Note Title"


def test_note_update(client, login):
    load_sample_notes(client, login)

    response = client.get(
        "/api/notes",
        headers={"x-access-tokens": login},
    )
    id = str(json.loads(response.data.decode())[0]["_id"]["$oid"])

    update_response = client.put(
        "/api/notes/" + id,
        data=json.dumps({"title": "Updated Title", "content": "Updated note content."}),
        headers={"x-access-tokens": login},
    )

    assert update_response.status_code == 200

    response = client.get(
        "/api/notes/" + id,
        headers={"x-access-tokens": login},
    )

    assert response.json["title"] == "Updated Title"
    assert response.json["content"] == "Updated note content."


def test_note_update_invalid_content(client, login):
    load_sample_notes(client, login)

    response = client.get(
        "/api/notes",
        headers={"x-access-tokens": login},
    )
    id = str(json.loads(response.data.decode())[0]["_id"]["$oid"])

    update_response = client.put(
        "/api/notes/" + id,
        data=json.dumps({"title": "Updated Title"}),
        headers={"x-access-tokens": login},
    )

    assert update_response.status_code == 400
    assert update_response.json["message"] == "Invalid request"


def test_note_update_note_not_found(client, login):
    load_sample_notes(client, login)

    response = client.get(
        "/api/notes",
        headers={"x-access-tokens": login},
    )
    id = str(json.loads(response.data.decode())[0]["_id"]["$oid"])

    update_response = client.put(
        "/api/notes/6460f1c46b46c376caa6ee2f",
        data=json.dumps({"title": "Updated Title", "content": "Updated note content."}),
        headers={"x-access-tokens": login},
    )

    assert update_response.status_code == 400
    assert update_response.json["message"] == "No updates applied, or note not found"


def test_note_delete(client, login):
    load_sample_notes(client, login)

    response = client.get(
        "/api/notes",
        headers={"x-access-tokens": login},
    )
    id = response.json[0]["_id"]["$oid"]

    delete_response = client.delete(
        "/api/notes/" + id,
        headers={"x-access-tokens": login},
    )

    assert delete_response.status_code == 200

    get_response = client.get(
        "/api/notes/" + id,
        headers={"x-access-tokens": login},
    )
    assert get_response.status_code == 404


def test_note_delete_note_not_found(client, login):
    load_sample_notes(client, login)

    delete_response = client.delete(
        "/api/notes/6460f1c46b46c376caa6ee2f",
        headers={"x-access-tokens": login},
    )

    assert delete_response.status_code == 404
    assert delete_response.json["message"] == "Note not found"


def test_note_share(client, login):
    load_sample_notes(client, login)

    response = client.get(
        "/api/notes",
        headers={"x-access-tokens": login},
    )
    note_id = response.json[0]["_id"]["$oid"]

    signup_response = client.post(
        "/api/auth/signup",
        data=json.dumps({"username": "test2", "password": "test"}),
    )
    new_user_id = signup_response.json["id"]

    login_response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "test2", "password": "test"}),
    )
    new_user_token = login_response.json["token"]

    share_response = client.post(
        "/api/notes/" + note_id + "/share",
        data=json.dumps({"shared_with": new_user_id}),
        headers={"x-access-tokens": login},
    )

    assert share_response.status_code == 200

    new_user_get_response = client.get(
        "/api/notes/" + note_id,
        headers={"x-access-tokens": new_user_token},
    )

    assert new_user_get_response.status_code == 200
    assert new_user_get_response.json["title"] == "1st Note Title"

    new_user_get_all_response = client.get(
        "/api/notes",
        headers={"x-access-tokens": new_user_token},
    )

    assert new_user_get_all_response.status_code == 200
    assert new_user_get_all_response.json[0]["title"] == "1st Note Title"


def test_note_share_note_not_found(client, login):
    load_sample_notes(client, login)

    share_response = client.post(
        "/api/notes/6460f1c46b46c376caa6ee2f/share",
        data=json.dumps({"shared_with": "6460f1c46b46c376caa6ee2f"}),
        headers={"x-access-tokens": login},
    )

    assert share_response.status_code == 404
    assert share_response.json["message"] == "Note not found"
