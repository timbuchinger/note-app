import json

from tests.conftest import load_sample_notes


def test_note_search_single_keyword(client, login):
    load_sample_notes(client, login)

    search_response = client.get(
        "/api/search?q=First",
        headers={"x-access-tokens": login},
    )

    assert search_response.status_code == 200
    assert len(json.loads(search_response.data.decode())) == 1
    assert json.loads(search_response.data.decode())[0]["title"] == "1st Note Title"


def test_note_search_multiple_keywords(client, login):
    load_sample_notes(client, login)

    search_response = client.get(
        "/api/search?q=First%202nd",
        headers={"x-access-tokens": login},
    )

    assert search_response.status_code == 200
    assert len(json.loads(search_response.data.decode())) == 2


def test_notes_not_found(client, login):
    load_sample_notes(client, login)

    search_response = client.get(
        "/api/search?q=Third",
        headers={"x-access-tokens": login},
    )

    assert search_response.status_code == 404
    assert json.loads(search_response.data.decode())["message"] == "No notes found"
