import json
import datetime

from app.models.friend import get_friends_by_user_id
from app.models.group import Group, insert_group
from app.models.group_member import GroupMember
from app.models.user import User, insert_user
from app.models.bill import (Bill, insert_bill,
                             get_bill_by_id)
from app.models.bill_member import BillMember
from app.util.json_data_encoder import json_data_encoder


def test_add_members_to_bill_if_bill_already_created(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 confirmed=True,
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
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 200
    assert json_response["message"] == "Updated bill"

    assert len(bill.members) == 3

    assert bill.members[0].user_id == user1.id
    assert bill.members[0].amount == data["members"][0]["amount"]

    assert bill.members[1].user_id == user2.id
    assert bill.members[1].amount == data["members"][1]["amount"]

    assert bill.members[2].user_id == user3.id
    assert bill.members[2].amount == data["members"][2]["amount"]


def test_delete_members_from_bill_if_bill_already_created(test_client,
                                                          api_headers_bearer,
                                                          insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 confirmed=True,
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
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert json_response["message"] == "Updated bill"

    assert len(bill.members) == 2

    assert bill.members[0].user_id == user1.id
    assert bill.members[0].amount == data["members"][0]["amount"]

    assert bill.members[1].user_id == user2.id
    assert bill.members[1].amount == data["members"][1]["amount"]


def test_change_description_of_existing_bill(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
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
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert json_response["message"] == "Updated bill"
    assert bill.description == data["description"]


def test_change_date_of_existing_bill(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

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
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data, default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 200
    assert json_response["message"] == "Updated bill"
    assert bill.date == data["date"]


def test_dont_change_date_created_of_existing_bill(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
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
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data, default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 400
    assert json_response["message"] == "Attribute date_created should not be set"
    assert bill.date_created == now


def test_dont_change_bill_if_amounts_sum_is_not_zero(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 confirmed=True,
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
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 400
    assert json_response["message"] == "Sum of amounts must be zero"
    assert len(bill.members) == 2
    assert bill.members[0].user_id == bill_member1.user_id
    assert bill.members[0].amount == bill_member1.amount
    assert bill.members[1].user_id == bill_member2.user_id
    assert bill.members[1].amount == bill_member2.amount


def test_delete_existing_bill(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 confirmed=True,
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
                                  headers=api_headers_bearer(
                                      user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Deleted bill"
    assert bill1.valid is False


def test_error_on_user_is_not_allowed_to_modify_bill(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user3)
    user3_tokens = insert_tokens(user3.email)

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
                               headers=api_headers_bearer(
                                   user3_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 401
    assert json_response["message"] == "Bill does not exist"
    assert bill.description == "Bill"


def test_error_on_user_is_not_allowed_to_modify_bill2(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user3)
    user3_tokens = insert_tokens(user3.email)

    group = Group(name="Group", group_members=[GroupMember(user=user1)])
    insert_group(group)

    bill_member1 = BillMember(user_id=user1.id, amount="5.00")
    bill_member2 = BillMember(user_id=user2.id, amount="-5.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 group=group,
                 members=[bill_member1, bill_member2])
    bill_id = insert_bill(bill1).id

    data = {
        "description": "New"
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_bearer(
                                   user3_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 401
    assert json_response["message"] == "Bill does not exist"
    assert bill.description == "Bill"


def test_group_member_is_allowed_to_modify_bill(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user3)
    user3_tokens = insert_tokens(user3.email)

    group = Group(name="Group", group_members=[GroupMember(user=user1),
                                               GroupMember(user=user3)])
    insert_group(group)

    bill_member1 = BillMember(user_id=user1.id, amount="5.00")
    bill_member2 = BillMember(user_id=user2.id, amount="-5.00")

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 group=group,
                 members=[bill_member1, bill_member2])
    bill_id = insert_bill(bill1).id

    data = {
        "description": "New"
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_bearer(
                                   user3_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 200
    assert json_response["message"] == "Updated bill"
    assert bill.description == data["description"]


def test_error_on_bill_not_existing(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
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

    response = test_client.put("/bills/2",
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 400
    assert json_response["message"] == "Bill does not exist"
    assert bill.description == "Bill"


def test_error_on_datetime_invalid_format(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
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
        "date": "a"
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data, default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 400
    assert json_response["message"] == "Cannot convert a to datetime"
    assert bill.date == now


def test_add_new_member_to_bill_add_member_as_friend_of_bill_members(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 confirmed=True,
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
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data))

    assert response.status_code == 200

    user1_friends = get_friends_by_user_id(user1.id)
    assert len(user1_friends) == 2
    assert user1_friends[0].friend_id == user2.id
    assert user1_friends[1].friend_id == user3.id

    user2_friends = get_friends_by_user_id(user2.id)
    assert len(user2_friends) == 2
    assert user2_friends[0].friend_id == user1.id
    assert user2_friends[1].friend_id == user3.id

    user3_friends = get_friends_by_user_id(user3.id)
    assert len(user3_friends) == 2
    assert user3_friends[0].friend_id == user1.id
    assert user3_friends[1].friend_id == user2.id


def test_add_unregistered_member_to_bill_if_bill_already_created(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
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
                "email": "newuser@mail.de",
                "amount": 6
            }
        ]
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 200
    assert json_response["message"] == "Updated bill"

    assert len(bill.members) == 3


def test_add_unregistered_member_to_bill_that_was_already_created(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 confirmed=True,
                 password=password)
    insert_user(user2)

    new_user_email = "newuser@mail.de"
    insert_user(User(email=new_user_email))

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
                "email": new_user_email,
                "amount": 6
            }
        ]
    }

    response = test_client.put("/bills/{}".format(bill_id),
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    bill = get_bill_by_id(bill_id)

    assert response.status_code == 200
    assert json_response["message"] == "Updated bill"

    assert len(bill.members) == 3


def test_needs_to_be_confirmed_on_delete(test_client, api_headers_bearer, insert_tokens):
    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password="secret")
    insert_user(user)
    tokens = insert_tokens(user.email)

    response = test_client.delete("/bills/1",
                                  headers=api_headers_bearer(
                                      tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 403
    assert json_response["message"] == "Account needs to be confirmed for this operation"


def test_needs_to_be_confirmed_on_put(test_client, api_headers_bearer, insert_tokens):
    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password="secret")
    insert_user(user)
    tokens = insert_tokens(user.email)

    response = test_client.put("/bills/1",
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 403
    assert json_response["message"] == "Account needs to be confirmed for this operation"
