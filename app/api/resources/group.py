from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.api.resources.common import (
    load_request_data_as_json, check_user_is_member_of_group,
    check_group_exists, get_attribute)
from app.common import get_authorized_user


def _load_group_data(json_data):
    get_attribute(json_data, "id", ttype=int)
    get_attribute(json_data, "name")
    members = get_attribute(json_data, "members", ttype=list)

    for member in members:
        get_attribute(member, "id", ttype=int)

    return json_data


def _update_group_data(group, data):
    if "name" in data:
        group.name = data["name"]


def _delete_group(group):
    group.valid = False

    for bill in group.bills:
        bill.valid = False


def _validate_group_data(data, group_id):
    if data["id"] != group_id:
        abort(400, "Group id's don't match")


class GroupResource(Resource):

    @jwt_required
    def put(self, group_id):
        json_data = load_request_data_as_json(request)

        data = _load_group_data(json_data)

        _validate_group_data(data, group_id)

        group = check_group_exists(group_id)

        check_user_is_member_of_group(get_authorized_user(), group)

        _update_group_data(group, data)

        return {"message": "Edited group"}, 200

    @jwt_required
    def delete(self, group_id):
        group = check_group_exists(group_id)

        check_user_is_member_of_group(get_authorized_user(), group)

        _delete_group(group)

        return {"message": "Deleted group"}, 200
