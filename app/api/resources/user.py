from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import get_user_by_id, get_user_by_email
from app.api.schemas.user import user_schema


def _is_user_allowed_to_access(user_id):
    authorized_user_email = get_jwt_identity()
    authorized_user_id = get_user_by_email(authorized_user_email).id

    if authorized_user_id != user_id:
        abort(401, "Not allowed to view user")


class UserResource(Resource):

    @jwt_required
    def get(self, user_id):
        _is_user_allowed_to_access(user_id)

        user = get_user_by_id(user_id)
        user_dumped = user_schema.dump(user)

        result = {
            "message": "Returned user",
            "user": user_dumped
        }

        return result, 200
