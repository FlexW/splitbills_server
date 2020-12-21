from flask import request, abort
from flask_restful import Resource
from app.models.user import User, insert_user, get_user_by_email
from app.api.resources.common import load_request_data_as_json, get_attribute


def _load_user_data_for_registration(json_data):
    email = get_attribute(json_data, "email")
    first_name = get_attribute(json_data, "first_name")
    last_name = get_attribute(json_data, "last_name")
    password = get_attribute(json_data, "password")

    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password
    }

    return data


def _check_user_does_not_exist(data):
    user = get_user_by_email(email=data["email"])

    if user is not None:
        abort(400, "User already exists")


def _create_new_user(data):

    user = User(first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                password=data["password"])

    insert_user(user)

    return user


class UsersResource(Resource):
    def post(self):
        json_data = load_request_data_as_json(request)

        data = _load_user_data_for_registration(json_data)

        _check_user_does_not_exist(data)

        user = _create_new_user(data)

        result = {
            "message": "Created new user",
            "user": user.to_dict()
        }

        return result, 201
