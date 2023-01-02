from flask_jwt_extended import jwt_required
from flask_restful import Resource
from app.api.resources.common import (check_user_is_member_of_group,
                                      check_user_exists,
                                      check_group_exists)
from app.common import get_authorized_user


def _delete_user_from_group(user, group):
    for member in group.group_members:
        if member.user_id == user.id:
            member.valid = 0


class GroupMemberResource(Resource):

    @jwt_required()
    def delete(self, group_id, user_id):
        group = check_group_exists(group_id)

        check_user_is_member_of_group(get_authorized_user(), group)

        user = check_user_exists(user_id)
        check_user_is_member_of_group(user, group)

        _delete_user_from_group(user, group)

        return {"message": "Deleted user from group"}, 200
