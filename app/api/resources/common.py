from flask import abort
from app.models.group import get_group_by_id
from app.models.user import get_user_by_id
from app.models.bill import get_bill_by_id


def check_bill_exists(bill_id):
    bill = get_bill_by_id(bill_id)

    if bill is None:
        abort(400, {"message": "Bill does not exist."})

    return bill


def load_request_data_as_json(request):
    json_data = request.get_json()

    if not json_data:
        abort(400, {"message": "No input data provided."})

    return json_data


def check_user_exists(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        abort(400, "User does not exist.")

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


def get_attribute(json_data, attribute, ttype=str):
    result = json_data.get(attribute)

    if result is None:
        abort(400, "Missing attribute {}".format(attribute))

    if type(result) != ttype:
        typestr = str(ttype)[8:]
        typestr = typestr[:len(typestr) - 2]
        abort(400, "Attribute {} needs to be of type {}".format(
            attribute, typestr))

    return result
