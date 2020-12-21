import json
import datetime

from app.models.bill import Bill, insert_bill
from app.models.bill_member import BillMember
from app.models.group import Group, insert_group
from app.models.user import User, insert_user
from app.models.group_member import GroupMember


def test_change_name_of_existing_group(test_client, api_headers_bearer, insert_tokens):
    password = "secretpassword"
    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)
    tokens = insert_tokens(user.email)
    group = Group(name="Name", group_members=[GroupMember(user=user)])
    insert_group(group)

    data = {
        "id": group.id,
        "name": "Changed",
        "members": [{"id": user.id}]
    }

    response = test_client.put("/groups/{}".format(group.id),
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Edited group"
    assert group.name == data["name"]


def test_error_on_group_ids_dont_match(test_client, api_headers_bearer, insert_tokens):
    password = "secretpassword"
    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)
    tokens = insert_tokens(user.email)
    group = Group(name="Name", group_members=[GroupMember(user=user)])
    insert_group(group)

    data = {
        "id": 2,
        "name": "Changed",
        "members": [{"id": user.id}]
    }

    response = test_client.put("/groups/{}".format(group.id),
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Group id's don't match"
    assert group.name == "Name"


def test_error_on_user_not_member_of_group(test_client, api_headers_bearer, insert_tokens):
    password = "secretpassword"
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
    user2_tokens = insert_tokens(user2.email)
    group = Group(name="Name", group_members=[GroupMember(user=user1)])
    insert_group(group)

    data = {
        "id": group.id,
        "name": "Changed",
        "members": [{"id": user1.id}]
    }

    response = test_client.put("/groups/{}".format(group.id),
                               headers=api_headers_bearer(
                                   user2_tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Group does not exist"
    assert group.name == "Name"


def test_delete_existing_group(test_client, api_headers_bearer, insert_tokens):
    password = "secretpassword"
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
    group = Group(name="Name", group_members=[GroupMember(user=user1),
                                              GroupMember(user=user2)])
    insert_group(group)

    bill_member1 = BillMember(user_id=user1.id, amount="5.00")
    bill_member2 = BillMember(user_id=user2.id, amount="-5.00")

    bill1 = Bill(description="Bill",
                 group=group,
                 date=now,
                 date_created=now,
                 members=[bill_member1, bill_member2])
    insert_bill(bill1)

    assert group.valid is True

    response = test_client.delete("/groups/{}".format(group.id),
                                  headers=api_headers_bearer(
                                      user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Deleted group"
    assert group.valid is False
    assert bill1.valid is False


def test_error_on_not_existing_group(test_client, api_headers_bearer, insert_tokens):
    password = "secretpassword"
    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)
    tokens = insert_tokens(user.email)

    data = {
        "id": 1,
        "name": "Changed",
        "members": [{"id": user.id}]
    }

    response = test_client.put("/groups/1",
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Group does not exist"


def test_needs_to_be_authenticated_on_put(test_client, api_headers):
    response = test_client.put("/groups/1", headers=api_headers)
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Missing Authorization Header"


def test_needs_to_be_authenticated_on_delete(test_client, api_headers):
    response = test_client.delete("/groups/1", headers=api_headers)
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Missing Authorization Header"
