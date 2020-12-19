from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.token import TokenNotFound, revoke_token, unrevoke_token
from app.api.resources.common import get_attribute
from app.api.resources.common import load_request_data_as_json


class TokenResource(Resource):
    @jwt_required
    def put(self, token_id):
        # Get and verify the desired revoked status from the body
        json_data = load_request_data_as_json(request)

        revoke = get_attribute(json_data, "revoke", ttype=bool)

        # Revoke or unrevoke the token based on what was passed to this function
        user_identity = get_jwt_identity()

        try:
            if revoke:
                revoke_token(token_id, user_identity)
                return {"message": "Token revoked"}, 200
            else:
                unrevoke_token(token_id, user_identity)
                return {"message": "Token unrevoked"}, 200
        except TokenNotFound:
            return {"message": "The specified token was not found"}, 404
