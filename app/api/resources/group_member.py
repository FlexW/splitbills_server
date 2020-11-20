from flask import request, g
from flask_restful import Resource
from app import auth
from .common import (load_request_data_as_json,
                     check_user_is_member_of_group,
                     check_user_exists,
                     check_group_exists)


def _load_group_id_data(json_data):
    if "group_id" in json_data and type(json_data["group_id"]) == int:
        return {"group_id": json_data["group_id"]}

    abort({"message": "Missing field 'group_id'."})

def _delete_user_from_group(user, group):
    for member in group.group_members:
        if member.user_id == user.id:
            member.valid = 0


class GroupMemberResource(Resource):

    @auth.login_required
    def delete(self, user_id):
        json_data = load_request_data_as_json(request)

        data = _load_group_id_data(json_data)

        group = check_group_exists(data["group_id"])

        check_user_is_member_of_group(g.current_user, group)

        user = check_user_exists(user_id)
        check_user_is_member_of_group(user, group)

        _delete_user_from_group(user, group)

        return {"message": "Deleted user from group."}
