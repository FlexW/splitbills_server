from flask import abort, request, g
from flask_restful import Resource
from marshmallow import ValidationError
from app.api.schemas.group import group_schema, groups_schema
from app.models.group import Group, insert_group, get_groups_by_user_id
from app.models.user import User, get_user_by_id
from app import auth
from .common import load_request_data_as_json


def _load_group_data(json_data):
    try:
        data = group_schema.load(json_data, partial=("id",
                                                     "members.password",
                                                     "members.first_name",
                                                     "members.last_name",
                                                     "members.email"))
    except ValidationError as error:
        abort({"message": "Could not find all required fields."})

    return data


def _validate_group(data):
    current_user = g.current_user
    is_current_user_in_group = False

    for member in data["members"]:
        # Check user exists
        user_id = member["id"]
        if not get_user_by_id(user_id):
            abort("User with id {} does not exist.".format(user_id))

        # Check if user is current user
        if user_id == current_user.id:
            is_current_user_in_group = True

    if not is_current_user_in_group:
        abort("User who created group must be group member.")


def _create_new_group(data):
    group = Group(name=data["name"])

    for member in data["members"]:
        user = get_user_by_id(member["id"])
        group.members.append(user)

    insert_group(group)

    return group

class GroupsResource(Resource):

    @auth.login_required
    def post(self):
        json_data = load_request_data_as_json(request)

        data = _load_group_data(json_data)

        _validate_group(data)

        group = _create_new_group(data)

        return {"message": "Created new group.", "group": group_schema.dump(group)}

    @auth.login_required
    def get(self):
        current_user = g.current_user

        groups = get_groups_by_user_id(current_user.id)

        return {"groups": groups_schema.dump(groups)}
