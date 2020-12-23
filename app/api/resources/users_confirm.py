from flask_jwt_extended import jwt_required
from flask_restful import Resource
from app.api.resources.common import get_authorized_user


class UsersConfirmResource(Resource):

    @jwt_required
    def put(self, token):
        user = get_authorized_user()

        if user.confirmed is True:
            return {"message": "Account already confirmed"}, 200

        if user.confirm(token):
            return {"message": "Acount confirmed"}, 201

        return {"message": "Confirmation token invalid"}, 400
