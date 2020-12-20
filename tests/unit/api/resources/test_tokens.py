import json

from app.models.user import User, insert_user
from app.models.token import get_user_tokens


def test_get_token(test_client, api_headers):
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

    assert response.status_code == 201

    assert "message" in json_response
    assert json_response["message"] == "Created access and refresh token"

    assert "access_token" in json_response
    assert "id" in json_response["access_token"]
    assert "token" in json_response["access_token"]

    assert "refresh_token" in json_response
    assert "id" in json_response["refresh_token"]
    assert "token" in json_response["refresh_token"]


def test_token_gets_saved(test_client, api_headers):
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

    test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))

    tokens = get_user_tokens(user.email)
    assert len(tokens) == 2
    assert tokens[0].revoked is False
    assert tokens[1].revoked is False


def test_tokens_are_different(test_client, api_headers):
    password = "secret"
    user1 = User(email="muster@mail.de",
                 password=password,
                 first_name="Max",
                 last_name="Muster")
    user2 = User(email="muster2@mail.de",
                 password=password,
                 first_name="Max",
                 last_name="Muster")
    insert_user(user1)
    insert_user(user2)

    data1 = {
        "email": user1.email,
        "password": password
    }
    data2 = {
        "email": user2.email,
        "password": password
    }

    response1 = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data1))
    json_response1 = json.loads(response1.get_data(as_text=True))
    response2 = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data2))
    json_response2 = json.loads(response2.get_data(as_text=True))

    assert json_response1["access_token"]["token"] != json_response2["access_token"]["token"]
    assert json_response1["refresh_token"]["token"] != json_response2["refresh_token"]["token"]


def test_dont_get_token_if_not_registered(test_client, api_headers):
    data = {
        "email": "muster@mail.de",
        "password": "secret"
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert "message" in json_response
    assert json_response["message"] == "Incorrect email or password"


def test_dont_get_token_if_password_incorrect(test_client, api_headers):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": password + "wrong"
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 403
    assert "message" in json_response
    assert json_response["message"] == "Incorrect email or password"


def test_error_on_password_missing(test_client, api_headers):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert "message" in json_response
    assert json_response["message"] == "Missing attribute password"


def test_error_on_password_wrong_type(test_client, api_headers):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": user.email,
        "password": True
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert "message" in json_response
    assert json_response["message"] == "Attribute password needs to be of type str"


def test_error_on_email_missing(test_client, api_headers):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert "message" in json_response
    assert json_response["message"] == "Missing attribute email"


def test_error_on_email_wrong_type(test_client, api_headers):
    password = "secret"
    user = User(email="muster@mail.de",
                password=password,
                first_name="Max",
                last_name="Muster")
    insert_user(user)

    data = {
        "email": True,
        "password": password
    }

    response = test_client.post(
        "/tokens", headers=api_headers, data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert "message" in json_response
    assert json_response["message"] == "Attribute email needs to be of type str"
