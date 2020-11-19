from flask_restful import Resource, abort
from app.models.user import get_user_by_id
from app.api.schemas.user import user_schema
from app import auth

def abort_if_user_doesnt_exist(user_id):
    if get_user_by_id(user_id) is None:
        abort(404, message="User with id {} doesn't exist".format(user_id))


class UserResource(Resource):

    @auth.login_required
    def get(self, user_id):
        abort_if_user_doesnt_exist(user_id)

        user = get_user_by_id(user_id)
        result = user_schema.dump(user)

        return result

    def put(self, user_id):
        pass
