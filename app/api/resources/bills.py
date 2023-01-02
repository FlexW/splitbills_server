from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.group import get_group_by_id
from app.models.bill_member import BillMember
from app.models.bill import Bill, insert_bill, get_valid_bills_by_user_id
from app.models.user import User, get_user_by_id, insert_user, get_user_by_email
from app.api.resources.common import (load_request_data_as_json,
                                      check_user_exists,
                                      check_group_exists,
                                      check_user_is_member_of_group,
                                      get_attribute,
                                      check_has_not_attribute,
                                      get_attribute_if_existing,
                                      convert_string_to_datetime,
                                      update_friends)
from app.common import get_authorized_user


def _load_bill_data(json_data):
    check_has_not_attribute(json_data, "id")
    check_has_not_attribute(json_data, "valid")

    description = get_attribute(json_data, "description")
    date = get_attribute_if_existing(json_data, "date")
    date_created = get_attribute_if_existing(json_data, "date_created")
    group_id = get_attribute_if_existing(json_data, "group_id", ttype=int)
    members = get_attribute(json_data, "members", ttype=list)

    data = {}
    data["description"] = description
    if date is not None:
        data["date"] = convert_string_to_datetime(date)

    if date_created is not None:
        data["date_created"] = convert_string_to_datetime(date_created)

    if group_id is not None:
        data["group_id"] = group_id

    data["members"] = []

    for member in members:
        member_id = get_attribute_if_existing(member, "user_id", ttype=int)
        if member_id is None:
            member_email = get_attribute(member, "email", ttype=str)
            user = get_user_by_email(member_email)
            if user is None:
                user = User(email=member_email)
                insert_user(user)
            member_id = user.id

        amount = get_attribute(member, "amount", ttype=int)

        data["members"].append({
            "user_id": member_id,
            "amount": amount
        })

    return data


def _validate_bill(data):
    amounts_sum = 0
    creditor_ids_in_group = []
    debtor_ids_in_group = []

    for member in data["members"]:
        user = check_user_exists(member["user_id"])
        amount = member["amount"]
        amounts_sum += amount

        if amount > 0:
            if user.id in creditor_ids_in_group:
                abort(400,
                      "User {} can only be one time a creditor".format(user.id))
            creditor_ids_in_group.append(user.id)
        else:
            if user.id in debtor_ids_in_group:
                abort(400,
                      "User {} can only be one time a debtor".format(user.id))
            debtor_ids_in_group.append(user.id)

    if amounts_sum != 0:
        abort(400, "Sum of amounts must be zero")

    if "group_id" in data:
        group = check_group_exists(data["group_id"])
        for member in data["members"]:
            check_user_is_member_of_group(
                get_user_by_id(member["user_id"]), group)


def _create_new_bill(data):
    bill = Bill(description=data["description"],
                date=data.get("date", None),
                date_created=data.get("date_created", None))

    for member in data["members"]:
        user = get_user_by_id(member["user_id"])
        bill_member = BillMember(user=user,
                                 bill=bill,
                                 amount=member["amount"])
        bill.members.append(bill_member)

    if "group_id" in data:
        bill.group = get_group_by_id(data["group_id"])

    insert_bill(bill)

    return bill


class BillsResource(Resource):

    @jwt_required()
    def post(self):
        json_data = load_request_data_as_json(request)

        data = _load_bill_data(json_data)

        _validate_bill(data)

        bill = _create_new_bill(data)

        user_id_list = [member["user_id"] for member in data["members"]]
        update_friends(user_id_list)

        return {
            "message": "Created new bill",
            "bill": bill.to_dict()
        }, 201

    @jwt_required()
    def get(self):
        current_user = get_authorized_user()

        bills = get_valid_bills_by_user_id(current_user.id)

        return {
            "message": "Returned bills",
            "bills": [bill.to_dict() for bill in bills]
        }, 200
