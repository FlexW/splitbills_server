from flask import abort, request, g
from flask_restful import Resource
from marshmallow import ValidationError
from app.api.schemas.group_add_user import group_add_user_schema
from app import auth
from app.models.user import get_user_by_id
from app.models.group import get_group_by_id
from app.models.group_member import GroupMember
from .common import load_request_data_as_json


def _check_group_exists(group_id):
    group = get_group_by_id(group_id)

    if group is None:
        abort({"message": "Group does not exist."})

    return group


def _check_user_is_member_of_group(user, group):
    for member in group.group_members:
        if member.user_id == user.id:
            return

    abort({"message": "Forbidden"})


def _check_user_exists(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        abort({"message": "User does not exist."})

    return user


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


class GroupAddUserResource(Resource):

    @auth.login_required
    def post(self):
        json_data = load_request_data_as_json(request)

        data = _load_group_add_user_data(json_data)

        group = _check_group_exists(data["group_id"])
        user = _check_user_exists(data["user_id"])

        _check_user_is_member_of_group(g.current_user, group)

        _check_user_is_not_already_member_of_group(user, group)

        _add_user_to_group(user, group)

        return {"message": "Added user to group."}
