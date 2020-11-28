import decimal

from flask import abort, request, g
from flask_restful import Resource
from marshmallow import ValidationError
from app import auth
from app.models.bill_member import BillMember
from app.api.schemas.bill import bill_schema
from app.api.resources.common import load_request_data_as_json, check_bill_exists


def _load_bill_data(json_data):
    try:
        data = bill_schema.load(json_data, partial=("id",
                                                    "description",
                                                    "date",
                                                    "date_created",
                                                    "group_id",
                                                    "members",
                                                    "members.bill_id"))
    except ValidationError:
        abort({"message": "Could not find all required fields."})

    return data


def _check_user_is_allowed_to_modify_bill(user, bill):
    for member in bill.members:
        if member.user == user:
            return

    for member in bill.group.group_members:
        if member.user == user:
            return

    abort({"message": "Forbidden"})


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

        # TODO: Delete members from bill


def _update_bill_data(bill, data):
    _update_description(bill, data)
    _update_date(bill, data)
    _update_bill_members(bill, data)


def _validate_bill_members_data(data):
    amount_sum = 0
    for members in data["members"]:
        amount_sum += members["amount"]

    if amount_sum != decimal.Decimal(0):
        abort({"message": "Sum of amounts must be zero."})


def _validate_bill_data(data):

    if "members" in data:
        _validate_bill_members_data(data)


def _delete_bill(bill):
    bill.valid = False


class BillResource(Resource):

    @auth.login_required
    def put(self, bill_id):
        json_data = load_request_data_as_json(request)

        bill = check_bill_exists(bill_id)

        data = _load_bill_data(json_data)

        _validate_bill_data(data)

        _check_user_is_allowed_to_modify_bill(g.current_user, bill)

        _update_bill_data(bill, data)

        return {"message": "Changed bill."}

    @auth.login_required
    def delete(self, bill_id):
        bill = check_bill_exists(bill_id)

        _check_user_is_allowed_to_modify_bill(g.current_user, bill)

        _delete_bill(bill)

        return {"message": "Deleted bill."}
