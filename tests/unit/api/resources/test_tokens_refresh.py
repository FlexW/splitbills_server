import json

from app.models.user import User, insert_user


def test_refresh_token(test_client, api_headers, api_headers_bearer):
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

    refresh_token = json_response["refresh_token"]

    response = test_client.post(
        "/tokens/refresh", headers=api_headers_bearer(refresh_token["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201

    assert "message" in json_response
    assert json_response["message"] == "Token refreshed"

    assert "access_token" in json_response
    assert "id" in json_response["access_token"]
    assert "token" in json_response["access_token"]


def test_dont_refresh_token_with_access_token(test_client, api_headers, api_headers_bearer):
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
        "/tokens/refresh", headers=api_headers_bearer(access_token["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 422
