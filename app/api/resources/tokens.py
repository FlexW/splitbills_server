from flask import abort, request, current_app
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from app.api.resources.common import load_request_data_as_json
from app.models.user import get_user_by_email
from app.models.token import add_token_to_database


def _get_attribute(json_data, attribute):
    result = json_data.get(attribute)
    if result is None:
        abort(400, "Missing attribute {}".format(attribute))
    return result


def _check_user_is_registered(email, password):
    error_code = 403
    error_response = "Incorrect email or password"

    user = get_user_by_email(email)

    if user is None:
        abort(error_code, error_response)

    if not user.verify_password(password):
        abort(error_code, error_response)

    return user


class TokensResource(Resource):
    def post(self):
        json_data = load_request_data_as_json(request)

        email = _get_attribute(json_data, "email")
        password = _get_attribute(json_data, "password")

        _check_user_is_registered(email, password)

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        add_token_to_database(
            access_token, current_app.config["JWT_IDENTITY_CLAIM"])
        add_token_to_database(
            refresh_token, current_app.config["JWT_IDENTITY_CLAIM"])

        result = {"access_token": access_token, "refresh_token": refresh_token}

        return result, 200
