import json

from app.models.group import Group, insert_group
from app.models.user import User, insert_user
from app.models.group_member import GroupMember


def test_change_name_of_existing_group(test_client, api_headers_auth):
    password = "secretpassword"
    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    insert_user(user)
    group = Group(name="Name", group_members=[GroupMember(user=user)])
    insert_group(group)

    data = {
        "name": "Changed"
    }

    response = test_client.put("/groups/{}".format(group.id),
                               headers=api_headers_auth(user.email, password),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Edited group."
    assert group.name == data["name"]


def test_dont_change_name_if_user_not_member_of_group(test_client, api_headers_auth):
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
    group = Group(name="Name", group_members=[GroupMember(user=user1)])
    insert_group(group)

    data = {
        "name": "Changed"
    }

    response = test_client.put("/groups/{}".format(group.id),
                               headers=api_headers_auth(user2.email, password),
                               data=json.dumps(data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Forbidden"
    assert group.name == "Name"


def test_delete_existing_group(test_client, api_headers_auth):
    password = "secretpassword"
    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    group = Group(name="Name", group_members=[GroupMember(user=user1)])
    insert_group(group)

    assert group.valid is True

    response = test_client.delete("/groups/{}".format(group.id),
                                  headers=api_headers_auth(user1.email, password))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Deleted group."
    assert group.valid is False
