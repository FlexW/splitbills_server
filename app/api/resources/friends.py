from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.friend import get_friends_by_user_id
from app.api.resources.common import get_authorized_user


class FriendsResource(Resource):

    @jwt_required
    def get(self):

        current_user = get_authorized_user()

        friends = get_friends_by_user_id(current_user.id)

        result = {
            "message": "Returned friends",
            "friends": [{"user_id": friend.friend_id} for friend in friends]
        }

        return result, 200
