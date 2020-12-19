from flask import abort, request, current_app
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from app.api.resources.common import get_attribute
from app.api.resources.common import load_request_data_as_json
from app.models.user import get_user_by_email
from app.models.token import add_token_to_database


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

        email = get_attribute(json_data, "email")
        password = get_attribute(json_data, "password")

        _check_user_is_registered(email, password)

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        access_token_id = add_token_to_database(
            access_token, current_app.config["JWT_IDENTITY_CLAIM"])
        refresh_token_id = add_token_to_database(
            refresh_token, current_app.config["JWT_IDENTITY_CLAIM"])

        result = {
            "access_token": {
                "id": access_token_id,
                "token":access_token
            },
            "refresh_token": {
                "id": refresh_token_id,
                "token": refresh_token
            }
        }

        return result, 200
