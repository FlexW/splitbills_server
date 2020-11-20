import pytest

from marshmallow.exceptions import ValidationError
from tests.common import not_raises
from app.api.schemas.group import group_schema


def test_load_valid_group_with_members():
    group_data = {
        "id": 1,
        "name": "Name",
        "members": [
            {
                "id": 1,
                "first_name": "Max",
                "last_name": "Muster",
                "email": "muster@mail.de",
                "password": "123"
            }
        ]
    }

    result = group_schema.load(group_data)

    assert result["id"] == 1
    assert result["name"] == "Name"
    assert result["members"][0]["id"] == 1


def test_dont_load_group_without_id():
    group_data = {
        "name": "Name",
        "members": [
            {
                "id": 1,
                "first_name": "Max",
                "last_name": "Muster",
                "email": "muster@mail.de",
                "password": "123"
            }
        ]
    }

    with pytest.raises(ValidationError):
        group_schema.load(group_data)


def test_dont_load_group_without_name():
    group_data = {
        "id": 1,
        "members": [
            {
                "id": 1,
                "first_name": "Max",
                "last_name": "Muster",
                "email": "muster@mail.de",
                "password": "123"
            }
        ]
    }

    with pytest.raises(ValidationError):
        group_schema.load(group_data)


def test_dont_load_group_without_members():
    group_data = {
        "id": 1,
        "name": "Name"
    }

    with pytest.raises(ValidationError):
        group_schema.load(group_data)
