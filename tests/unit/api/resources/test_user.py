import pytest
import json

from app.models.user import User, insert_user


def test_user_can_get_itself(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)
    tokens = insert_tokens(user.email)

    response = test_client.get("/users/{}".format(user.id),
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200

    assert json_response["message"] == "Returned user"

    assert json_response["user"]["id"] == user.id
    assert json_response["user"]["first_name"] == user.first_name
    assert json_response["user"]["last_name"] == user.last_name
    assert json_response["user"]["email"] == user.email
    with pytest.raises(KeyError):
        json_response["user"]["password"]


def test_user_can_get_only_itself(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)
    user2_tokens = insert_tokens(user2.email)

    response = test_client.get("/users/{}".format(user2.id),
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Not allowed to view user"


def test_needs_to_be_authenticated(test_client, api_headers):
    response = test_client.get("/users/1", headers=api_headers)
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Missing Authorization Header"
