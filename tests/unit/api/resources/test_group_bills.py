import json
import datetime

from app.models.group_member import GroupMember
from app.models.group import Group, insert_group
from app.models.user import User, insert_user
from app.models.bill import (Bill,
                             insert_bill,
                             get_bills_by_user_id,
                             get_all_bills)
from app.models.bill_member import BillMember


def test_get_bills_from_group(test_client, api_headers_auth):
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

    bill = Bill(description="Bill",
                date=now,
                date_created=now,
                group=group,
                members=[BillMember(user=user1, amount=3),
                         BillMember(user=user2, amount=-3)])
    insert_bill(bill)

    response = test_client.get("/groups/{}/bills".format(group.id),
                               headers=api_headers_auth(user1.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 1
    assert json_response["bills"][0]["id"] == bill.id


def test_get_only_bills_from_group(test_client, api_headers_auth):
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
                               headers=api_headers_auth(user1.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert len(json_response["bills"]) == 1
    assert json_response["bills"][0]["id"] == bill1.id
