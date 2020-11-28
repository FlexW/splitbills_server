import json
import datetime
import decimal

from app.models.group_member import GroupMember
from app.models.group import Group, insert_group
from app.models.user import User, insert_user
from app.models.bill import (Bill, insert_bill,
                             get_bills_by_user_id,
                             get_all_bills,
                             get_bill_by_id)
from app.models.bill_member import BillMember
from app.util.json_data_encoder import json_data_encoder


def test_add_bill(app, test_client, api_headers_auth):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_data = {
        "description": "Important bill",
        "date": now,
        "date_created": now,
        "members": [
            {
                "user_id": user1.id,
                "amount": "20.00"
            },
            {
                "user_id": user2.id,
                "amount": "-20.00"
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_auth(
                                    user1.email, password),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Created new bill."
    assert len(get_bills_by_user_id(user1.id)) == 1
    assert len(get_bills_by_user_id(user2.id)) == 1

    bill = get_bills_by_user_id(user1.id)[0]
    assert bill.description == bill_data["description"]
    assert bill.date == bill_data["date"]
    assert bill.date_created == bill_data["date_created"]
    assert bill.members[0].user == user1
    assert (bill.members[0].amount
            == decimal.Decimal(bill_data["members"][0]["amount"]))
    assert bill.members[1].user == user2
    assert (bill.members[1].amount
            == decimal.Decimal(bill_data["members"][1]["amount"]))


def test_add_bill_in_group(app, test_client, api_headers_auth):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    group = Group(name="Name",
                  group_members=[GroupMember(user=user1), GroupMember(user=user2)])
    insert_group(group)

    bill_data = {
        "description": "Important bill",
        "date": now,
        "date_created": now,
        "group_id": group.id,
        "members": [
            {
                "user_id": user1.id,
                "amount": "20.00"
            },
            {
                "user_id": user2.id,
                "amount": "-20.00"
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_auth(
                                    user1.email, password),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Created new bill."
    assert len(get_bills_by_user_id(user1.id)) == 1
    assert len(get_bills_by_user_id(user2.id)) == 1

    bill = get_bills_by_user_id(user1.id)[0]
    assert bill.group == group


def test_dont_add_bill_if_amounts_sum_not_zero(test_client, api_headers_auth):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_data = {
        "description": "Important bill",
        "date": now,
        "date_created": now,
        "members": [
            {
                "user_id": user1.id,
                "amount": "20.00"
            },
            {
                "user_id": user2.id,
                "amount": "-20.01"
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_auth(
                                    user1.email, password),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Sum of amounts must be zero."
    assert len(get_all_bills()) == 0


def test_get_bills_from_user(app, test_client, api_headers_auth):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)

    bill_member1 = BillMember(user_id=user.id, amount="1.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now)
    insert_bill(bill1)
    bill_member1.bill = bill1
    bill1.members.append(bill_member1)

    bill_member2 = BillMember(user_id=user.id, amount="1.00")

    bill2 = Bill(description="Bill2",
                 date=now,
                 date_created=now)
    insert_bill(bill2)
    bill_member2.bill = bill2

    response = test_client.get("/bills",
                               headers=api_headers_auth(user.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 2
    assert json_response["bills"][0]["description"] == bill1.description
    assert json_response["bills"][1]["description"] == bill2.description


def test_get_just_bills_from_user(app, test_client, api_headers_auth):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_member1 = BillMember(user_id=user1.id, amount="1.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now)
    insert_bill(bill1)
    bill_member1.bill = bill1
    bill1.members.append(bill_member1)

    bill_member2 = BillMember(user_id=user2.id, amount="1.00")

    bill2 = Bill(description="Bill2",
                 date=now,
                 date_created=now)
    insert_bill(bill2)
    bill_member2.bill = bill2

    response = test_client.get("/bills",
                               headers=api_headers_auth(user1.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 1
    assert json_response["bills"][0]["description"] == bill1.description


def test_get_only_not_removed_bills(test_client, api_headers_auth):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill1 = Bill(description="Bill",
                 members=[BillMember(user=user1, amount="-2.00"),
                          BillMember(user=user2, amount="2.00")],
                 date=now,
                 date_created=now)
    insert_bill(bill1)

    bill2 = Bill(description="Bill",
                 members=[BillMember(user=user1, amount="-2.00"),
                          BillMember(user=user2, amount="2.00")],
                 date=now,
                 date_created=now,
                 valid=False)
    insert_bill(bill2)

    response = test_client.get("/bills",
                               headers=api_headers_auth(user1.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 1
    assert json_response["bills"][0]["id"] == bill1.id
