import json

from app.models.user import User, insert_user, get_all_users
from app.models.group import Group, insert_group, get_group_by_id, get_all_groups
from app.models.group_member import GroupMember


def test_delete_user_from_existing_group(test_client, api_headers_auth):
    password = "securepassword"

    user1 = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user1 = insert_user(user1)

    group_member1 = GroupMember(user=user1)
    group = Group(name="Muster",
                  group_members=[group_member1])
    insert_group(group)

    group_data = {
        "group_id": group.id
    }

    response = test_client.delete("/groups/members/{}".format(user1.id),
                                  headers=api_headers_auth(user1.email, password),
                                  data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Deleted user from group."
    assert group_member1.valid == 0


def test_dont_delete_user_if_user_not_in_group(test_client, api_headers_auth):
    password = "securepassword"

    user1 = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user1 = insert_user(user1)

    user2 = User(first_name="Max",
                last_name="Muster",
                email="muster2@mail.de",
                password=password)
    user2 = insert_user(user2)

    group_member1 = GroupMember(user=user1)
    group = Group(name="Muster",
                  group_members=[group_member1])
    insert_group(group)

    group_data = {
        "group_id": group.id
    }

    response = test_client.delete("/groups/members/{}".format(user1.id),
                                  headers=api_headers_auth(user2.email, password),
                                  data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Forbidden"
    assert group_member1.valid == 1


def test_dont_delete_user_if_no_group_id_given(test_client, api_headers_auth):
    password = "securepassword"

    user1 = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user1 = insert_user(user1)

    group_member1 = GroupMember(user=user1)
    group = Group(name="Muster",
                  group_members=[group_member1])
    insert_group(group)

    group_data = {}

    response = test_client.delete("/groups/members/{}".format(user1.id),
                                  headers=api_headers_auth(user1.email, password),
                                  data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "No input data provided."
    assert group_member1.valid == 1


def test_dont_delete_user_if_not_in_group(test_client, api_headers_auth):
    password = "securepassword"

    user1 = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user1 = insert_user(user1)

    user2 = User(first_name="Max",
                last_name="Muster",
                email="muster2@mail.de",
                password=password)
    user2 = insert_user(user2)

    group_member1 = GroupMember(user=user1)
    group = Group(name="Muster",
                  group_members=[group_member1])
    insert_group(group)

    group_data = {
        "group_id": group.id
    }

    response = test_client.delete("/groups/members/{}".format(user2.id),
                                  headers=api_headers_auth(user1.email, password),
                                  data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Forbidden"
    assert group_member1.valid == 1
    assert len(group.group_members) == 1
