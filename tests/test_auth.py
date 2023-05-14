import json


def test_signup_successful(client):
    response = client.post(
        "/api/auth/signup",
        data=json.dumps({"username": "test", "password": "test"}),
    )
    assert b"id" in response.data
    assert response.status_code == 200


def test_signup_duplicate_user(client, signup):
    response = client.post(
        "/api/auth/signup",
        data=json.dumps({"username": "test", "password": "test2"}),
    )
    assert b"User already exists" in response.data
    assert response.status_code == 400


def test_login_successful(client, signup):
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "test", "password": "test"}),
    )
    assert b"token" in response.data
    assert response.status_code == 200


def test_login_invalid_username(client, signup):
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "invalid_user", "password": "test"}),
    )
    assert b"Invalid credentials provided" in response.data
    assert response.status_code == 401


def test_login_invalid_password(client, signup):
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "test", "password": "invalid_password"}),
    )
    assert b"Invalid credentials provided" in response.data
    assert response.status_code == 401


def test_login_missing_data(client, signup):
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "test"}),
    )
    assert b"Incomplete credentials provided" in response.data
    assert response.status_code == 401


def test_auth_no_token(client):
    response = client.get(
        "/api/notes",
    )
    assert response.status_code == 400
    assert response.json["message"] == "A token must be provided"


def test_auth_invalid_token(client):
    response = client.get("/api/notes", headers={"x-access-tokens": "abc123"})
    assert response.status_code == 400
    assert response.json["message"] == "The provided token is invalid"
