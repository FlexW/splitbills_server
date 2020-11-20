from flask import request, abort
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from app import db
from app.models.user import User, insert_user, get_user_by_email
from app.api.schemas.user import user_schema, users_schema
from .common import load_request_data_as_json


def _load_user_data_for_registration(json_data):
    try:
        data = user_schema.load(json_data, partial=("id",))
    except ValidationError as error:
        abort({"message": "Could not find all required fields."})

    return data


def _check_user_does_not_exist(data):
    try:
        user = get_user_by_email(email=data["email"])
    except KeyError as error:
        abort({"message": "Could not find field {}.".format(str(error))})

    if user is not None:
        abort({"message": "User already exists."})


def _create_new_user(data):
    try:
        user = User(first_name=data["first_name"],
                    last_name=data["last_name"],
                    email=data["email"],
                    password=data["password"])
    except KeyError as error:
        abort({"message": "Could not find field {}.".format(str(error))})
    insert_user(user)

    return user


class UsersResource(Resource):
    def post(self):
        json_data = load_request_data_as_json(request)

        data = _load_user_data_for_registration(json_data)

        _check_user_does_not_exist(data)

        user = _create_new_user(data)

        result = user_schema.dump(User.query.get(user.id))

        return {"message": "Created new user.", "user": result}
