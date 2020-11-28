from flask import abort, request, g
from flask_restful import Resource
from marshmallow import ValidationError
from app import auth
from .common import (load_request_data_as_json,
                     check_user_is_member_of_group,
                     check_group_exists)
from app.api.schemas.group import group_schema


def _load_group_data(json_data):
    try:
        data = group_schema.load(json_data, partial=("id",
                                                     "name",
                                                     "members"))
    except ValidationError:
        abort({"message": "Could not find all required fields."})

    return data


def _update_group_data(group, data):
    if "name" in data:
        group.name = data["name"]


def _delete_group(group):
    group.valid = False


class GroupResource(Resource):

    @auth.login_required
    def put(self, group_id):
        json_data = load_request_data_as_json(request)

        data = _load_group_data(json_data)

        group = check_group_exists(group_id)

        check_user_is_member_of_group(g.current_user, group)

        _update_group_data(group, data)

        return {"message": "Edited group."}

    @auth.login_required
    def delete(self, group_id):
        group = check_group_exists(group_id)

        check_user_is_member_of_group(g.current_user, group)

        _delete_group(group)

        return {"message": "Deleted group."}
