from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.user import get_user_by_id
from app.api.resources.common import get_authorized_user


def _is_user_allowed_to_access(user_id):
    authorized_user_id = get_authorized_user().id

    if authorized_user_id != user_id:
        abort(401, "Not allowed to view user")


class UserResource(Resource):

    @jwt_required
    def get(self, user_id):
        _is_user_allowed_to_access(user_id)

        user = get_user_by_id(user_id)

        result = {
            "message": "Returned user",
            "user": user.to_dict()
        }

        return result, 200
