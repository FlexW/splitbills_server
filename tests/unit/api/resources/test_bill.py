import json
import datetime


from app.models.user import User, insert_user
from app.models.bill import (Bill, insert_bill,
                             get_bill_by_id)
from app.models.bill_member import BillMember
from app.util.json_data_encoder import json_data_encoder


def test_add_members_to_bill_if_bill_already_created(test_client, api_headers_auth):
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

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 password=password)
    insert_user(user3)

    bill_member1 = BillMember(user_id=user1.id, amount="5.00")
    bill_member2 = BillMember(user_id=user2.id, amount="-5.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 members=[bill_member1, bill_member2])
    bill_id = insert_bill(bill1).id

    data = {
        "members": [
            {
                "user_id": user1.id,
                "amount": -3
            },
            {
                "user_id": user2.id,
                "amount": -3
            },
            {
                "user_id": user3.id,
                "amount": 6
            }
        ]
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_auth(user1.email, password),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert json_response["message"] == "Changed bill."

    assert len(bill.members) == 3

    assert bill.members[0].user_id == user1.id
    assert bill.members[0].amount == data["members"][0]["amount"]

    assert bill.members[1].user_id == user2.id
    assert bill.members[1].amount == data["members"][1]["amount"]

    assert bill.members[2].user_id == user3.id
    assert bill.members[2].amount == data["members"][2]["amount"]


def test_delete_members_from_bill_if_bill_already_created(test_client,
                                                          api_headers_auth):
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

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 password=password)
    insert_user(user3)

    bill_member1 = BillMember(user_id=user1.id, amount=-3)
    bill_member2 = BillMember(user_id=user2.id, amount=-3)
    bill_member3 = BillMember(user_id=user3.id, amount=6)

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 members=[bill_member1, bill_member2, bill_member3])
    bill_id = insert_bill(bill1).id

    data = {
        "members": [
            {
                "user_id": user1.id,
                "amount": 5
            },
            {
                "user_id": user2.id,
                "amount": -5
            }
        ]
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_auth(user1.email, password),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert json_response["message"] == "Changed bill."

    assert len(bill.members) == 2

    assert bill.members[0].user_id == user1.id
    assert bill.members[0].amount == data["members"][0]["amount"]

    assert bill.members[1].user_id == user2.id
    assert bill.members[1].amount == data["members"][1]["amount"]


def test_change_description_of_existing_bill(test_client, api_headers_auth):
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

    bill_member1 = BillMember(user_id=user1.id, amount="5.00")
    bill_member2 = BillMember(user_id=user2.id, amount="-5.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 members=[bill_member1, bill_member2])
    bill_id = insert_bill(bill1).id

    data = {
        "description": "New"
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_auth(user1.email, password),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert json_response["message"] == "Changed bill."
    assert bill.description == data["description"]


def test_change_date_of_existing_bill(test_client, api_headers_auth):
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

    bill_member1 = BillMember(user_id=user1.id, amount="5.00")
    bill_member2 = BillMember(user_id=user2.id, amount="-5.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 members=[bill_member1, bill_member2])
    bill_id = insert_bill(bill1).id

    data = {
        "date": datetime.datetime.utcnow()
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_auth(user1.email, password),
                               data=json.dumps(data, default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert json_response["message"] == "Changed bill."
    assert bill.date == data["date"]


def test_dont_change_date_created_of_existing_bill(test_client, api_headers_auth):
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

    bill_member1 = BillMember(user_id=user1.id, amount="5.00")
    bill_member2 = BillMember(user_id=user2.id, amount="-5.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 members=[bill_member1, bill_member2])
    bill_id = insert_bill(bill1).id

    data = {
        "date_created": datetime.datetime.utcnow()
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_auth(user1.email, password),
                               data=json.dumps(data, default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert json_response["message"] == "Changed bill."
    assert bill.date_created == now


def test_dont_change_bill_if_amounts_sum_is_not_zero(test_client, api_headers_auth):
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

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 password=password)
    insert_user(user3)

    bill_member1 = BillMember(user_id=user1.id, amount=5)
    bill_member2 = BillMember(user_id=user2.id, amount=-5)

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 members=[bill_member1, bill_member2])
    bill_id = insert_bill(bill1).id

    data = {
        "members": [
            {
                "user_id": user1.id,
                "amount": -4
            },
            {
                "user_id": user2.id,
                "amount": -3
            },
            {
                "user_id": user3.id,
                "amount": 6
            }
        ]
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_auth(user1.email, password),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert json_response["message"] == "Sum of amounts must be zero."
    assert len(bill.members) == 2
    assert bill.members[0].user_id == bill_member1.user_id
    assert bill.members[0].amount == bill_member1.amount
    assert bill.members[1].user_id == bill_member2.user_id
    assert bill.members[1].amount == bill_member2.amount


def test_delete_existing_bill(test_client, api_headers_auth):
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

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 password=password)
    insert_user(user3)

    bill_member1 = BillMember(user_id=user1.id, amount="5.00")
    bill_member2 = BillMember(user_id=user2.id, amount="-5.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 members=[bill_member1, bill_member2])
    bill_id = insert_bill(bill1).id

    assert bill1.valid is True

    response = test_client.delete("/bills/{}".format(bill_id),
                                  headers=api_headers_auth(user1.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Deleted bill."
    assert bill1.valid is False
