import json
import datetime

from app.models.group_member import GroupMember
from app.models.group import Group, insert_group
from app.models.user import User, insert_user
from app.models.bill import Bill, insert_bill
from app.models.bill_member import BillMember


def test_get_bills_from_group(test_client, api_headers_bearer, insert_tokens):
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

    bill = Bill(description="Bill",
                date=now,
                date_created=now,
                group=group,
                members=[BillMember(user=user1, amount=3),
                         BillMember(user=user2, amount=-3)])
    insert_bill(bill)

    response = test_client.get("/groups/{}/bills".format(group.id),
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Returned bills"
    assert len(json_response["bills"]) == 1
    assert json_response["bills"][0]["id"] == bill.id


def test_get_only_bills_from_group(test_client, api_headers_bearer, insert_tokens):
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

    bill1 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 group=group,
                 members=[BillMember(user=user1, amount=3),
                          BillMember(user=user2, amount=-3)])
    insert_bill(bill1)
    bill2 = Bill(description="Bill",
                 date=now,
                 date_created=now,
                 members=[BillMember(user=user1, amount=3),
                          BillMember(user=user2, amount=-3)])
    insert_bill(bill2)

    response = test_client.get("/groups/{}/bills".format(group.id),
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 1
    assert json_response["bills"][0]["id"] == bill1.id


def test_needs_to_be_authenticated_on_get(test_client, api_headers):
    response = test_client.get("/groups/1/bills", headers=api_headers)
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Missing Authorization Header"
