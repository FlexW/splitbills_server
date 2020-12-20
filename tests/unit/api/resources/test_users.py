import pytest
import json

from app.models.user import get_user_by_email, get_all_users


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

    assert json_respone["message"] == "Created new user"
    assert json_respone["user"]["id"] == 1
    assert json_respone["user"]["first_name"] == user_data["first_name"]
    assert json_respone["user"]["last_name"] == user_data["last_name"]
    assert json_respone["user"]["email"] == user_data["email"]
    with pytest.raises(KeyError):
        json_respone["user"]["password"]

    assert response.status_code == 201
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

    assert response.status_code == 400
    assert json_respone["message"] == "User already exists"
    assert len(get_all_users()) == 1


def test_error_on_first_name_missing(app, test_client, api_headers):
    user_data = {
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_respone["message"] == "Missing attribute first_name"
    assert len(get_all_users()) == 0


def test_error_on_first_name_wrong_type(app, test_client, api_headers):
    user_data = {
        "first_name": True,
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_respone["message"] == "Attribute first_name needs to be of type str"
    assert len(get_all_users()) == 0


def test_error_on_last_name_missing(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "email": "muster@mail.de",
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_respone["message"] == "Missing attribute last_name"
    assert len(get_all_users()) == 0


def test_error_on_last_name_wrong_type(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "last_name": True,
        "email": "muster@mail.de",
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_respone["message"] == "Attribute last_name needs to be of type str"
    assert len(get_all_users()) == 0


def test_error_on_email_missing(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "last_name": "Muster",
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_respone["message"] == "Missing attribute email"
    assert len(get_all_users()) == 0


def test_error_on_email_wrong_type(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "last_name": "Muster",
        "email": True,
        "password": "securepassword"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_respone["message"] == "Attribute email needs to be of type str"
    assert len(get_all_users()) == 0


def test_error_on_password_missing(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "last_name": "Muster",
        "email": "muster@mail.de"
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_respone["message"] == "Missing attribute password"
    assert len(get_all_users()) == 0


def test_error_on_password_wrong_type(app, test_client, api_headers):
    user_data = {
        "first_name": "Max",
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": True
    }

    response = test_client.post("/users",
                                headers=api_headers,
                                data=json.dumps(user_data))
    json_respone = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_respone["message"] == "Attribute password needs to be of type str"
    assert len(get_all_users()) == 0
