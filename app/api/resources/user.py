from flask_restful import Resource, abort
from app.models.user import get_user_by_id
from app.api.schemas.user import user_schema
from app import auth


class UserResource(Resource):

    @auth.login_required
    def get(self, user_id):
        user = get_user_by_id(user_id)
        result = user_schema.dump(user)

        return result
