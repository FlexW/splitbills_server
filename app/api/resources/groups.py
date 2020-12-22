from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.group import Group, insert_group, get_valid_groups_by_user_id
from app.models.user import User, get_user_by_id, get_user_by_email, insert_user
from app.models.group_member import GroupMember
from app.api.resources.common import (load_request_data_as_json,
                                      get_authorized_user,
                                      get_attribute,
                                      get_attribute_if_existing,
                                      update_friends)


def _load_group_data(json_data):
    get_attribute(json_data, "name")
    members = get_attribute(json_data, "members", ttype=list)

    for member in members:
        id = get_attribute_if_existing(member, "id", ttype=int)
        email = get_attribute_if_existing(member, "email", ttype=str)

        if id is None and email is None:
            abort(400, "Attribute id or email needs to be set")

    return json_data


def _get_user_from_member_data(member_data):
    if "email" in member_data:
        email = member_data["email"]
        user = get_user_by_email(email)

        if not user:
            # Create user
            user = insert_user(User(email=email))
            return user

        return user

    id = member_data["id"]
    user = get_user_by_id(id)

    if not user:
        abort(400, "User with id {} does not exist".format(id))

    return user


def _validate_group(data):
    current_user = get_authorized_user()
    is_current_user_in_group = False

    if "members" in data:
        for member in data["members"]:
            user = _get_user_from_member_data(member)

            # Check if user is current user
            if user.id == current_user.id:
                is_current_user_in_group = True

    if not is_current_user_in_group:
        abort(400, "User who created group must be group member")


def _create_new_group(data):
    group = Group(name=data["name"])

    for member in data["members"]:
        user = _get_user_from_member_data(member)

        group_member = GroupMember(user=user, group=group)

        group.group_members.append(group_member)

    insert_group(group)

    return group


class GroupsResource(Resource):

    @jwt_required
    def post(self):
        json_data = load_request_data_as_json(request)

        data = _load_group_data(json_data)

        _validate_group(data)

        group = _create_new_group(data)

        user_id_list = [_get_user_from_member_data(member).id for member in data["members"]]
        update_friends(user_id_list)

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
