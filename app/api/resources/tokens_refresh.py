from flask import current_app
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_refresh_token_required, get_jwt_identity, create_access_token)
from app.models.token import add_token_to_database


class TokensRefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        access_token_id = add_token_to_database(
            access_token, current_app.config['JWT_IDENTITY_CLAIM'])

        result = {
            "message": "Token refreshed",

            "access_token": {
                "id": access_token_id,
                "token": access_token
            }
        }

        return result, 201
