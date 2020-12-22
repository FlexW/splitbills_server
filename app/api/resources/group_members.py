from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.user import User, insert_user, get_user_by_email
from app.models.group_member import GroupMember
from app.api.resources.common import (load_request_data_as_json,
                                      check_user_exists,
                                      check_user_is_member_of_group,
                                      check_group_exists,
                                      get_authorized_user,
                                      get_attribute,
                                      get_attribute_if_existing,
                                      update_friends)


def _load_group_add_user_data(json_data):

    user_id = get_attribute_if_existing(json_data, "user_id", ttype=int)
    if user_id is None:
        email = get_attribute(json_data, "email")
        user = get_user_by_email(email)
        if user is None:
            user = User(email=email)
            insert_user(user)
        json_data["user_id"] = user.id

    return json_data


def _check_user_is_not_already_member_of_group(user, group):
    for member in group.group_members:
        if member.user_id == user.id:
            abort(400, "User is already in group")


def _add_user_to_group(user, group):
    group.group_members.append(GroupMember(user=user))


class GroupMembersResource(Resource):

    @jwt_required
    def post(self, group_id):
        json_data = load_request_data_as_json(request)

        data = _load_group_add_user_data(json_data)

        group = check_group_exists(group_id)
        user = check_user_exists(data["user_id"])

        current_user = get_authorized_user()

        check_user_is_member_of_group(current_user, group)

        _check_user_is_not_already_member_of_group(user, group)

        _add_user_to_group(user, group)

        update_friends([current_user.id, data["user_id"]])

        return {"message": "Added user to group"}, 201
