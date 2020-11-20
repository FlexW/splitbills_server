import pytest
import json

from app.models.user import User, get_user_by_email, get_all_users, insert_user
from app.api.schemas.user import user_schema


def test_add_non_existing_user(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert json_respone["message"] == "Created new user."
    assert json_respone["user"]["id"] == 1
    assert json_respone["user"]["first_name"] == user_data["first_name"]
    assert json_respone["user"]["last_name"] == user_data["last_name"]
    assert json_respone["user"]["email"] == user_data["email"]
    with pytest.raises(KeyError):
        json_respone["user"]["password"]

    assert get_user_by_email(user_data["email"]) is not None


def test_dont_add_existing_user(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": "securepassword"
    }

    test_client.post("/users",
                     headers=api_headers,
                     data=json.dumps(user_data))

    user_data2 = {
        "first_name": "Maxi",
        "last_name": "Mustermann",
        "email": "muster@mail.de",
        "password": "securepassword2"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data2))
    json_respone = json.loads(response.get_data(as_text=True))

    assert json_respone["message"] == "User already exists."
    assert len(get_all_users()) == 1


def test_dont_add_user_without_first_name(app, test_client, api_headers):
    user_data = {
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert json_respone["message"] == "Could not find all required fields."
    assert len(get_all_users()) == 0


def test_dont_add_user_without_last_name(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "email": "muster@mail.de",
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert json_respone["message"] == "Could not find all required fields."
    assert len(get_all_users()) == 0


def test_dont_add_user_without_email(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "last_name": "Muster",
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert json_respone["message"] == "Could not find all required fields."
    assert len(get_all_users()) == 0


def test_dont_add_user_without_password(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "last_name": "Muster",
        "email": "muster@mail.de"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert json_respone["message"] == "Could not find all required fields."
    assert len(get_all_users()) == 0
