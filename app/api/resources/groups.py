from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.group import Group, insert_group, get_valid_groups_by_user_id
from app.models.user import get_user_by_id
from app.models.friend import Friend, is_friend_with_user
from app.models.group_member import GroupMember
from app.api.resources.common import (
    load_request_data_as_json, get_authorized_user, get_attribute)


def _load_group_data(json_data):
    get_attribute(json_data, "name")
    members = get_attribute(json_data, "members", ttype=list)

    for member in members:
        get_attribute(member, "id", ttype=int)

    return json_data


def _validate_group(data):
    current_user = get_authorized_user()
    is_current_user_in_group = False

    if "members" in data:
        for member in data["members"]:
            # Check user exists
            user_id = member["id"]
            if not get_user_by_id(user_id):
                abort(400, "User with id {} does not exist".format(user_id))

            # Check if user is current user
            if user_id == current_user.id:
                is_current_user_in_group = True

    if not is_current_user_in_group:
        abort(400, "User who created group must be group member")


def _create_new_group(data):
    group = Group(name=data["name"])

    for member in data["members"]:
        user = get_user_by_id(member["id"])

        group_member = GroupMember(user=user, group=group)

        group.group_members.append(group_member)

    insert_group(group)

    return group


def _update_friends(data):
    for member in data["members"]:
        user = get_user_by_id(member["id"])
        for member in data["members"]:
            if user.id == member["id"]:
                continue
            if not is_friend_with_user(user.id, member["id"]):
                user.friends.append(Friend(friend=get_user_by_id(member["id"])))


class GroupsResource(Resource):

    @jwt_required
    def post(self):
        json_data = load_request_data_as_json(request)

        data = _load_group_data(json_data)

        _validate_group(data)

        group = _create_new_group(data)

        _update_friends(data)

        result = {
            "message": "Created new group",
            "group": group.to_dict()
        }

        return result, 201

    @jwt_required
    def get(self):
        current_user = get_authorized_user()

        groups = get_valid_groups_by_user_id(current_user.id)

        result = {
            "message": "Returned groups",
            "groups": [group.to_dict() for group in groups]
        }

        return result, 200
