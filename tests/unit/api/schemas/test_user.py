import pytest

from marshmallow.exceptions import ValidationError
from tests.common import not_raises
from app.api.schemas.user import user_schema


def test_load_valid_user():
    user_data = {
        "id": 1,
        "first_name": "Max",
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": "123"
    }

    with not_raises(ValidationError):
        user_schema.load(user_data)


def test_dont_load_user_without_id():
    user_data = {
        "first_name": "Max",
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": "123"
    }

    with pytest.raises(ValidationError):
        user_schema.load(user_data)


def test_dont_load_user_without_email():
    user_data = {
        "id": 1,
        "first_name": "Max",
        "last_name": "Muster",
        "password": "123"
    }

    with pytest.raises(ValidationError):
        user_schema.load(user_data)


def test_dont_load_user_without_password():
    user_data = {
        "id": 1,
        "first_name": "Max",
        "last_name": "Muster",
        "email": "muster@mail.de"
    }

    with pytest.raises(ValidationError):
        user_schema.load(user_data)


def test_dont_load_user_without_first_name():
    user_data = {
        "id": 1,
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": "123"
    }

    with pytest.raises(ValidationError):
        user_schema.load(user_data)


def test_dont_load_user_without_last_name():
    user_data = {
        "id": 1,
        "first_name": "Max",
        "email": "muster@mail.de",
        "password": "123"
    }

    with pytest.raises(ValidationError):
        user_schema.load(user_data)


def test_dump_user():
    user_data = {
        "id": 1,
        "first_name": "Max",
        "last_name": "Muster",
        "email": "muster@mail.de",
        "password": "123"
    }


    user_data = user_schema.load(user_data)
    result = user_schema.dump(user_data)

    assert result["id"] == 1
    assert result["first_name"] == "Max"
    assert result["last_name"] == "Muster"
    assert result["email"] == "muster@mail.de"

    with pytest.raises(KeyError):
        result["password"]
