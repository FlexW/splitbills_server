import json

from flask_jwt_extended import decode_token
from app.models.user import User, insert_user
from app.models.token import is_token_revoked, revoke_token


def test_revoke_access_token(test_client, api_headers, api_headers_bearer):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    access_token = json_response["access_token"]

    data = {
        "revoke": True
    }

    response = test_client.put("/tokens/{}".format(access_token["id"]),
                               headers=api_headers_bearer(access_token["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Token revoked"
    assert is_token_revoked(decode_token(access_token["token"])) is True


def test_unrevoke_access_token(test_client, api_headers, api_headers_bearer):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    access_token = json_response["access_token"]

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    second_access_token = json_response["access_token"]

    revoke_token(access_token["id"], user.email)

    data = {
        "revoke": False
    }

    response = test_client.put("/tokens/{}".format(access_token["id"]),
                               headers=api_headers_bearer(second_access_token["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Token unrevoked"
    assert is_token_revoked(decode_token(access_token["token"])) is False


def test_revoke_refresh_token(test_client, api_headers, api_headers_bearer):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    access_token = json_response["access_token"]
    refresh_token = json_response["refresh_token"]

    data = {
        "revoke": True
    }

    response = test_client.put("/tokens/{}".format(refresh_token["id"]),
                               headers=api_headers_bearer(access_token["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Token revoked"
    assert is_token_revoked(decode_token(refresh_token["token"])) is True


def test_unrevoke_refresh_token(test_client, api_headers, api_headers_bearer):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    access_token = json_response["access_token"]
    refresh_token = json_response["refresh_token"]

    revoke_token(refresh_token["id"], user.email)

    data = {
        "revoke": False
    }

    response = test_client.put("/tokens/{}".format(refresh_token["id"]),
                               headers=api_headers_bearer(access_token["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Token unrevoked"
    assert is_token_revoked(decode_token(refresh_token["token"])) is False


def test_revoked_token_is_invalid(test_client, api_headers, api_headers_bearer):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    access_token = json_response["access_token"]
    refresh_token = json_response["refresh_token"]

    revoke_token(access_token["id"], user.email)

    data = {
        "revoke": False
    }

    response = test_client.put("/tokens/{}".format(refresh_token["id"]),
                               headers=api_headers_bearer(access_token["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert is_token_revoked(decode_token(refresh_token["token"])) is False


def test_error_on_revoke_missing(test_client, api_headers, api_headers_bearer):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    access_token = json_response["access_token"]

    data = {"bla": 1}

    response = test_client.put("/tokens/{}".format
                               (access_token["id"]),
                               headers=api_headers_bearer(access_token["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Missing attribute revoke"
    assert is_token_revoked(decode_token(access_token["token"])) is False


def test_error_on_revoke_wrong_type(test_client, api_headers, api_headers_bearer):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    access_token = json_response["access_token"]

    data = {"revoke": 1}

    response = test_client.put("/tokens/{}".format
                               (access_token["id"]),
                               headers=api_headers_bearer(access_token["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Attribute revoke needs to be of type bool"
    assert is_token_revoked(decode_token(access_token["token"])) is False


def test_error_on_token_not_found(test_client, api_headers, api_headers_bearer):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    access_token = json_response["access_token"]

    data = {"revoke": True}

    response = test_client.put("/tokens/3",
                               headers=api_headers_bearer(access_token["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 404
    assert json_response["message"] == "The specified token was not found"
