from dateutil.parser import ParserError
from flask import abort
from flask_jwt_extended import get_jwt_identity
from app.util.converter import string_to_datetime
from app.models.group import get_group_by_id
from app.models.user import get_user_by_id, get_user_by_email
from app.models.bill import get_bill_by_id


def check_bill_exists(bill_id):
    bill = get_bill_by_id(bill_id)

    if bill is None:
        abort(400, "Bill does not exist")

    return bill


def load_request_data_as_json(request):
    json_data = request.get_json()

    if not json_data:
        abort(400, "No input data provided")

    return json_data


def check_user_exists(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        abort(400, "User does not exist")

    return user


def check_user_is_member_of_group(user, group):
    for member in group.group_members:
        if member.user_id == user.id:
            return

    abort(401, "Group does not exist")


def check_group_exists(group_id):
    group = get_group_by_id(group_id)

    if group is None:
        abort(401, "Group does not exist")

    return group


def check_attribute_has_correct_type(attribute, attribute_name, ttype=str):
    if type(attribute) != ttype:
        typestr = str(ttype)[8:]
        typestr = typestr[:len(typestr) - 2]
        abort(400, "Attribute {} needs to be of type {}".format(
            attribute_name, typestr))


def get_attribute(json_data, attribute, ttype=str):
    result = json_data.get(attribute)

    if result is None:
        abort(400, "Missing attribute {}".format(attribute))

    check_attribute_has_correct_type(result, attribute, ttype)

    return result


def check_has_not_attribute(json_data, attribute):
    if attribute in json_data:
        abort(400, "Attribute {} should not be set".format(attribute))


def get_attribute_if_existing(json_data, attribute, ttype=str):
    result = json_data.get(attribute)

    if result is None:
        return None

    check_attribute_has_correct_type(result, attribute, ttype)

    return result


def convert_string_to_datetime(datetime_str):
    try:
        date = string_to_datetime(datetime_str)
    except ParserError:
        abort(400, "Cannot convert {} to datetime".format(datetime_str))

    return date


def get_authorized_user():
    authorized_user_email = get_jwt_identity()
    authorized_user = get_user_by_email(authorized_user_email)

    return authorized_user
