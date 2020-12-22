from flask_restful import Resource
from flask_jwt_extended import jwt_required


class FriendsResource(Resource):

    @jwt_required
    def get(self):

        result = {
            "message": "Returned friends",
            "friends": []
        }

        return result, 200
