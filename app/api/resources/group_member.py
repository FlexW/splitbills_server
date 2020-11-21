from flask import abort, request, g
from flask_restful import Resource
from app import auth
from .common import (load_request_data_as_json,
                     check_user_is_member_of_group,
                     check_user_exists,
                     check_group_exists)


def _delete_user_from_group(user, group):
    for member in group.group_members:
        if member.user_id == user.id:
            member.valid = 0


class GroupMemberResource(Resource):

    @auth.login_required
    def delete(self, group_id, user_id):
        group = check_group_exists(group_id)

        check_user_is_member_of_group(g.current_user, group)

        user = check_user_exists(user_id)
        check_user_is_member_of_group(user, group)

        _delete_user_from_group(user, group)

        return {"message": "Deleted user from group."}
