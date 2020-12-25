import decimal

from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.user import User, insert_user, get_user_by_email
from app.models.bill_member import BillMember
from app.api.resources.common import (load_request_data_as_json,
                                      check_bill_exists,
                                      get_attribute,
                                      get_attribute_if_existing,
                                      check_has_not_attribute,
                                      convert_string_to_datetime,
                                      update_friends)
from app.decorators import confirmation_required
from app.common import get_authorized_user


def _load_bill_data(json_data):
    check_has_not_attribute(json_data, "date_created")
    check_has_not_attribute(json_data, "id")
    check_has_not_attribute(json_data, "valid")
    check_has_not_attribute(json_data, "group_id")

    description = get_attribute_if_existing(json_data, "description")
    date = get_attribute_if_existing(json_data, "date")
    members = get_attribute_if_existing(json_data, "members", ttype=list)

    data = {}

    if description is not None:
        data["description"] = description

    if date is not None:
        data["date"] = convert_string_to_datetime(date)

    if members is not None:
        data["members"] = []

        for member in members:
            member_id = get_attribute_if_existing(member, "user_id", ttype=int)

            if member_id is None:
                email = get_attribute(member, "email")
                user = get_user_by_email(email)
                if user is None:
                    user = User(email=email)
                    insert_user(user)
                member_id = user.id

            amount = get_attribute(member, "amount", ttype=int)

            data["members"].append({
                "user_id": member_id,
                "amount": amount
            })

    return data


def _check_user_is_allowed_to_modify_bill(user, bill):
    error_code = 401
    error_message = "Bill does not exist"

    for member in bill.members:
        if member.user == user:
            return

    if bill.group is None:
        abort(error_code, error_message)

    for member in bill.group.group_members:
        if member.user == user:
            return

    abort(error_code, error_message)


def _update_description(bill, data):
    if "description" in data:
        bill.description = data["description"]


def _update_date(bill, data):
    if "date" in data:
        bill.date = data["date"]


def _get_bill_member_by_id(bill, user_id):
    for member in bill.members:
        if member.user_id == user_id:
            return member

    return None


def _update_bill_members(bill, data):
    if "members" in data:

        # Remove members that are in bill but not in new bill.
        i = 0
        while i < len(bill.members):

            found = False
            for m in data["members"]:
                if m["user_id"] == bill.members[i].user_id:
                    found = True
                    break
            if found:
                i += 1
                continue
            del bill.members[i]

        # Update members that are already in group.
        i = 0
        while i < len(data["members"]):
            member = data["members"][0]
            bill_member = _get_bill_member_by_id(bill, member["user_id"])

            if bill_member is not None:
                bill_member.amount = member["amount"]
                del data["members"][i]
                i -= 1

            i += 1

        # Add the rest.
        for member in data["members"]:
            bill_member = BillMember(user_id=member["user_id"],
                                     bill_id=bill.id,
                                     amount=member["amount"])
            bill.members.append(bill_member)


def _update_bill_data(bill, data):
    _update_description(bill, data)
    _update_date(bill, data)
    _update_bill_members(bill, data)


def _validate_bill_members_data(data):
    amount_sum = 0
    for members in data["members"]:
        amount_sum += members["amount"]

    if amount_sum != decimal.Decimal(0):
        abort(400, "Sum of amounts must be zero")


def _validate_bill_data(data):

    if "members" in data:
        _validate_bill_members_data(data)


def _delete_bill(bill):
    bill.valid = False


def _update_friends(bill):
    user_id_list = [member.user_id for member in bill.members]
    update_friends(user_id_list)


class BillResource(Resource):

    @jwt_required
    @confirmation_required
    def put(self, bill_id):
        json_data = load_request_data_as_json(request)

        bill = check_bill_exists(bill_id)

        data = _load_bill_data(json_data)

        _validate_bill_data(data)

        _check_user_is_allowed_to_modify_bill(get_authorized_user(), bill)

        _update_bill_data(bill, data)

        _update_friends(bill)

        return {"message": "Updated bill"}, 200

    @jwt_required
    @confirmation_required
    def delete(self, bill_id):
        bill = check_bill_exists(bill_id)

        _check_user_is_allowed_to_modify_bill(get_authorized_user(), bill)

        _delete_bill(bill)

        return {"message": "Deleted bill"}, 200
