from flask import abort
from app.models.group import get_group_by_id
from app.models.user import get_user_by_id


def load_request_data_as_json(request):
    json_data = request.get_json()

    if not json_data:
        abort({"message": "No input data provided."})

    return json_data


def check_user_exists(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        abort({"message": "User does not exist."})

    return user


def check_user_is_member_of_group(user, group):
    for member in group.group_members:
        if member.user_id == user.id:
            return

    abort({"message": "Forbidden"})


def check_group_exists(group_id):
    group = get_group_by_id(group_id)

    if group is None:
        abort({"message": "Group does not exist."})

    return group