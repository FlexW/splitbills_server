from flask import abort, g
from flask_restful import Resource
from app import auth
from app.models.user import get_user_by_id
from app.api.schemas.user import user_schema


def _is_user_allowed_to_access(user_id):
    if g.current_user.id != user_id:
        abort({"message": "Forbidden"})


class UserResource(Resource):

    @auth.login_required
    def get(self, user_id):
        _is_user_allowed_to_access(user_id)

        user = get_user_by_id(user_id)
        result = user_schema.dump(user)

        return result
