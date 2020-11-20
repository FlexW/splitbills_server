import pytest
import json

from app.models.user import User, insert_user


def test_user_can_get_itself(app, test_client, api_headers_auth):
    password = "securepassword"
    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)

    response = test_client.get("/users/{}".format(user.id),
                                headers=api_headers_auth(user.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["id"] == user.id
    assert json_response["first_name"] == user.first_name
    assert json_response["last_name"] == user.last_name
    assert json_response["email"] == user.email
    with pytest.raises(KeyError):
        json_response["password"]


def test_user_can_get_only_itself(app, test_client, api_headers_auth):
    password = "securepassword"
    user1 = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    response = test_client.get("/users/{}".format(user2.id),
                                headers=api_headers_auth(user1.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Forbidden"
