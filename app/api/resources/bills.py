import decimal

from flask import abort, request, g
from flask_restful import Resource
from marshmallow import ValidationError
from app import auth
from app.api.schemas.bill import bill_schema, bills_schema
from app.models.group import get_group_by_id
from app.models.bill_member import BillMember
from app.models.bill import Bill, insert_bill, get_bills_by_user_id
from app.models.user import get_user_by_id
from .common import (load_request_data_as_json,
                     check_user_exists,
                     check_group_exists,
                     check_user_is_member_of_group)


def _load_bill_data(json_data):
    try:
        data = bill_schema.load(json_data, partial=("id",
                                                    "date",
                                                    "date_required",
                                                    "members.bill_id"))
    except ValidationError as error:
        abort({"message": "Could not find all required fields."})

    return data


def _validate_bill(data):
    amounts_sum = decimal.Decimal(0)
    creditor_ids_in_group = []
    debtor_ids_in_group = []

    for member in data["members"]:
        user = check_user_exists(member["user_id"])
        amount = decimal.Decimal(member["amount"])
        amounts_sum += amount

        if amount > 0:
            if user.id in creditor_ids_in_group:
                abort({"message": "User can only be one time a creditor."})
            creditor_ids_in_group.append(user.id)
        else:
            if user.id in debtor_ids_in_group:
                abort({"message": "User can only be one time a debtor."})
            debtor_ids_in_group.append(user.id)

    if amounts_sum != 0:
        abort({"message": "Sum of amounts must be zero."})

    if "group_id" in data:
        group = check_group_exists(data["group_id"])
        for member in data["members"]:
            check_user_is_member_of_group(get_user_by_id(member["user_id"]), group)


def _create_new_bill(data):
    bill = Bill(description=data["description"],
                date=data.get("date", None),
                date_created=data.get("date_created", None))

    for member in data["members"]:
        user = get_user_by_id(member["user_id"])
        bill_member = BillMember(user=user,
                                 bill=bill,
                                 amount=decimal.Decimal(member["amount"]))
        bill.members.append(bill_member)

    if "group_id" in data:
        bill.group = get_group_by_id(data["group_id"])

    insert_bill(bill)

    return bill


class BillsResource(Resource):

    @auth.login_required
    def post(self):
        json_data = load_request_data_as_json(request)

        data = _load_bill_data(json_data)

        _validate_bill(data)

        bill = _create_new_bill(data)

        return {"message": "Created new bill."}

    @auth.login_required
    def get(self):
        current_user = g.current_user

        bills = get_bills_by_user_id(current_user.id)

        return {"bills": bills_schema.dump(bills)}
