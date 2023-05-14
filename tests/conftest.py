import json
import os

import pytest

from project import create_app
from project.extensions import mongo


@pytest.fixture()
def app():
    os.environ[
        "MONGO_URI"
    ] = "mongodb://admin:password@localhost:27017/?authMechanism=DEFAULT"
    app = create_app()

    mongo["users"].delete_many({})
    mongo["notes"].delete_many({})

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def signup(client):
    response = client.post(
        "/api/auth/signup",
        data=json.dumps({"username": "test", "password": "test"}),
    )
    return json.loads(response.data.decode())["id"]


@pytest.fixture()
def login(client, signup):
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "test", "password": "test"}),
    )
    return json.loads(response.data.decode())["token"]


def load_sample_notes(client, login):
    client.post(
        "/api/notes",
        data=json.dumps({"title": "1st Note Title", "content": "First note content."}),
        headers={"x-access-tokens": login},
    )
    client.post(
        "/api/notes",
        data=json.dumps({"title": "2nd Note title", "content": "Second note content."}),
        headers={"x-access-tokens": login},
    )
