import json
import datetime

from app.util.converter import datetime_to_string, string_to_datetime
from app.models.group_member import GroupMember
from app.models.friend import get_friends_by_user_id
from app.models.group import Group, insert_group
from app.models.user import User, insert_user
from app.models.bill import (Bill,
                             insert_bill,
                             get_bills_by_user_id,
                             get_all_bills)
from app.models.bill_member import BillMember
from app.util.json_data_encoder import json_data_encoder


def test_add_bill(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_data = {
        "description": "Important bill",
        "date": datetime_to_string(now),
        "date_created": datetime_to_string(now),
        "members": [
            {
                "user_id": user1.id,
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -200
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201

    bill = get_bills_by_user_id(user1.id)[0]

    assert json_response["message"] == "Created new bill"
    assert json_response["bill"]["id"] == bill.id
    assert json_response["bill"]["description"] == bill.description
    assert json_response["bill"]["date"] == bill_data["date"]
    assert json_response["bill"]["date_created"] == bill_data["date_created"]

    assert len(get_bills_by_user_id(user1.id)) == 1
    assert len(get_bills_by_user_id(user2.id)) == 1

    assert bill.description == bill_data["description"]
    assert bill.date == string_to_datetime(bill_data["date"])
    assert bill.date_created == string_to_datetime(bill_data["date_created"])
    assert bill.members[0].user == user1
    assert (bill.members[0].amount
            == bill_data["members"][0]["amount"])
    assert bill.members[1].user == user2
    assert (bill.members[1].amount
            == bill_data["members"][1]["amount"])


def test_add_bill_without_date(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_data = {
        "description": "Important bill",
        "members": [
            {
                "user_id": user1.id,
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -200
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201

    bill = get_bills_by_user_id(user1.id)[0]

    assert json_response["message"] == "Created new bill"
    assert json_response["bill"]["id"] == bill.id
    assert json_response["bill"]["description"] == bill.description

    assert len(get_bills_by_user_id(user1.id)) == 1
    assert len(get_bills_by_user_id(user2.id)) == 1

    assert bill.description == bill_data["description"]
    assert bill.members[0].user == user1
    assert (bill.members[0].amount
            == bill_data["members"][0]["amount"])
    assert bill.members[1].user == user2
    assert (bill.members[1].amount
            == bill_data["members"][1]["amount"])


def test_add_bill_in_group(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    group = Group(name="Name",
                  group_members=[GroupMember(user=user1),
                                 GroupMember(user=user2)])
    insert_group(group)

    bill_data = {
        "description": "Important bill",
        "date": now,
        "date_created": now,
        "group_id": group.id,
        "members": [
            {
                "user_id": user1.id,
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -200
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert json_response["message"] == "Created new bill"
    assert len(get_bills_by_user_id(user1.id)) == 1
    assert len(get_bills_by_user_id(user2.id)) == 1

    bill = get_bills_by_user_id(user1.id)[0]
    assert bill.group == group


def test_dont_add_bill_if_amounts_sum_not_zero(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

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
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -201
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Sum of amounts must be zero"
    assert len(get_all_bills()) == 0


def test_get_bills_from_user(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)
    user_tokens = insert_tokens(user.email)

    bill_member1 = BillMember(user_id=user.id, amount=1)

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now)
    insert_bill(bill1)
    bill_member1.bill = bill1
    bill1.members.append(bill_member1)

    bill_member2 = BillMember(user_id=user.id, amount=1)

    bill2 = Bill(description="Bill2",
                 date=now,
                 date_created=now)
    insert_bill(bill2)
    bill_member2.bill = bill2

    response = test_client.get("/bills",
                               headers=api_headers_bearer(
                                   user_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Returned bills"
    assert len(json_response["bills"]) == 2
    assert json_response["bills"][0]["description"] == bill1.description
    assert json_response["bills"][1]["description"] == bill2.description


def test_get_just_bills_from_user(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

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
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 1
    assert json_response["bills"][0]["description"] == bill1.description


def test_get_only_not_removed_bills(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

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
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 1
    assert json_response["bills"][0]["id"] == bill1.id


def test_error_on_description_missing(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_data = {
        "date": now,
        "date_created": now,
        "members": [
            {
                "user_id": user1.id,
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -200
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Missing attribute description"
    assert len(get_all_bills()) == 0


def test_error_on_member_is_more_than_one_time_creditor(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_data = {
        "description": "Important bill",
        "date": datetime_to_string(now),
        "date_created": datetime_to_string(now),
        "members": [
            {
                "user_id": user1.id,
                "amount": 100
            },
            {
                "user_id": user1.id,
                "amount": 100
            },
            {
                "user_id": user2.id,
                "amount": -200
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "User {} can only be one time a creditor".format(user1.id)
    assert len(get_all_bills()) == 0


def test_error_on_member_is_more_than_one_time_debtor(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_data = {
        "description": "Important bill",
        "date": datetime_to_string(now),
        "date_created": datetime_to_string(now),
        "members": [
            {
                "user_id": user1.id,
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -100
            },
            {
                "user_id": user2.id,
                "amount": -100
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "User {} can only be one time a debtor".format(user2.id)
    assert len(get_all_bills()) == 0


def test_insert_friends_of_user_after_adding_bill(test_client, api_headers_bearer, insert_tokens):
    now = datetime.datetime.utcnow()
    password = "securepassword"

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

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

    bill_data = {
        "description": "Important bill",
        "date": datetime_to_string(now),
        "date_created": datetime_to_string(now),
        "members": [
            {
                "user_id": user1.id,
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -100
            },
            {
                "user_id": user3.id,
                "amount": -100
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data))

    assert response.status_code == 201

    # Get friends of user1
    friends_user1 = get_friends_by_user_id(user1.id)
    assert len(friends_user1) == 2
    assert friends_user1[0].friend_id == user2.id
    assert friends_user1[1].friend_id == user3.id

    # Get friends of user2
    friends_user2 = get_friends_by_user_id(user2.id)
    assert len(friends_user2) == 2
    assert friends_user2[0].friend_id == user1.id
    assert friends_user2[1].friend_id == user3.id

    # Get friends of user3
    friends_user3 = get_friends_by_user_id(user3.id)
    assert len(friends_user3) == 2
    assert friends_user3[0].friend_id == user1.id
    assert friends_user3[1].friend_id == user2.id


def test_can_create_multiple_times_bill_with_same_members(test_client, api_headers_bearer, insert_tokens):
    now = datetime.datetime.utcnow()
    password = "securepassword"

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

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

    bill_data = {
        "description": "Important bill",
        "date": datetime_to_string(now),
        "date_created": datetime_to_string(now),
        "members": [
            {
                "user_id": user1.id,
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -100
            },
            {
                "user_id": user3.id,
                "amount": -100
            }
        ]
    }

    # Create bill first time
    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data))

    assert response.status_code == 201

    # Create bill second time
    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data))

    assert response.status_code == 201


def test_create_bill_with_not_registered_bill_member(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    bill_data = {
        "description": "Important bill",
        "date": datetime_to_string(now),
        "date_created": datetime_to_string(now),
        "members": [
            {
                "user_id": user1.id,
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -100
            },
            {
                "email": "newuser@mail.de",
                "amount": -100
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201

    bill = get_bills_by_user_id(user1.id)[0]

    assert json_response["message"] == "Created new bill"

    assert len(get_bills_by_user_id(user1.id)) == 1
    assert len(get_bills_by_user_id(user2.id)) == 1

    assert len(bill.members) == 3


def test_create_bill_with_not_registered_bill_member_that_was_already_created(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"
    now = datetime.datetime.utcnow()

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    new_user_email = "newuser@mail.de"
    insert_user(User(email=new_user_email))

    bill_data = {
        "description": "Important bill",
        "date": datetime_to_string(now),
        "date_created": datetime_to_string(now),
        "members": [
            {
                "user_id": user1.id,
                "amount": 200
            },
            {
                "user_id": user2.id,
                "amount": -100
            },
            {
                "email": new_user_email,
                "amount": -100
            }
        ]
    }

    response = test_client.post("/bills",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(bill_data,
                                                default=json_data_encoder))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201

    bill = get_bills_by_user_id(user1.id)[0]

    assert json_response["message"] == "Created new bill"

    assert len(get_bills_by_user_id(user1.id)) == 1
    assert len(get_bills_by_user_id(user2.id)) == 1

    assert len(bill.members) == 3
