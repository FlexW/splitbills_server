from flask import abort, request, g
from flask_restful import Resource
from marshmallow import ValidationError
from app.api.schemas.group_add_user import group_add_user_schema
from app import auth
from app.models.user import get_user_by_id
from app.models.group import get_group_by_id
from app.models.group_member import GroupMember
from .common import (load_request_data_as_json,
                     check_user_exists,
                     check_user_is_member_of_group,
                     check_group_exists)


def _load_group_add_user_data(json_data):
    try:
        data = group_add_user_schema.load(json_data)
    except ValidationError as error:
        abort({"message": "Could not find all required fields."})

    return data


def _check_user_is_not_already_member_of_group(user, group):
    for member in group.group_members:
        if member.user_id == user.id:
            abort({"message": "User is already in group."})


def _add_user_to_group(user, group):
    group.group_members.append(GroupMember(user=user))


class GroupMembersResource(Resource):

    @auth.login_required
    def post(self, group_id):
        json_data = load_request_data_as_json(request)

        data = _load_group_add_user_data(json_data)

        group = check_group_exists(group_id)
        user = check_user_exists(data["user_id"])

        check_user_is_member_of_group(g.current_user, group)

        _check_user_is_not_already_member_of_group(user, group)

        _add_user_to_group(user, group)

        return {"message": "Added user to group."}
