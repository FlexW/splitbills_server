import json

from app.models.user import User, insert_user, get_all_users
from app.models.group import Group, insert_group, get_group_by_id, get_all_groups
from app.models.group_member import GroupMember


def test_add_user_to_existing_group(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    user1 = insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    user2 = insert_user(user2)

    group_member1 = GroupMember(user=user1)
    group = Group(name="Muster",
                  group_members=[group_member1])
    insert_group(group)

    group_add_user_data = {
        "user_id": user2.id,
    }

    response = test_client.post("/groups/{}/members".format(group.id),
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert json_response["message"] == "Added user to group"

    group = get_group_by_id(group.id)

    assert len(group.group_members) == 2


def test_dont_add_user_if_group_not_exist(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_add_user_data = {
        "user_id": user.id,
    }

    response = test_client.post("/groups/1/members",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Group does not exist"
    assert len(get_all_groups()) == 0


def test_dont_add_user_if_user_not_exist(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_member = GroupMember(user=user)
    group = Group(name="Group",
                  group_members=[group_member])
    insert_group(group)

    group_add_user_data = {
        "user_id": 2,
    }

    response = test_client.post("/groups/{}/members".format(group.id),
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "User does not exist"
    assert len(get_all_users()) == 1


def test_dont_add_user_if_user_already_in_group(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    user1 = insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    user2 = insert_user(user2)

    group_member1 = GroupMember(user=user1)
    group_member2 = GroupMember(user=user2)
    group = Group(name="Group",
                  group_members=[group_member1, group_member2])
    insert_group(group)

    group_add_user_data = {
        "user_id": user2.id,
    }

    response = test_client.post("/groups/{}/members".format(group.id),
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "User is already in group"
    assert len(group.group_members) == 2


def test_dont_add_user_if_user_not_in_group(test_client, api_headers_bearer, insert_tokens):
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
    user2_tokens = insert_tokens(user2.email)
    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 password=password)
    user3 = insert_user(user3)

    group_member1 = GroupMember(user=user1)
    group = Group(name="Group",
                  group_members=[group_member1])
    insert_group(group)

    group_add_user_data = {
        "user_id": user3.id,
    }

    response = test_client.post("/groups/{}/members".format(group.id),
                                headers=api_headers_bearer(
                                    user2_tokens["access_token"]["token"]),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Group does not exist"
    assert len(group.group_members) == 1


def test_dont_add_user_if_user_id_missing(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    user_tokens = insert_tokens(user.email)

    group = Group(name="Group")
    insert_group(group)

    group_add_user_data = {"bla": "bla"}

    response = test_client.post("/groups/{}/members".format(group.id),
                                headers=api_headers_bearer(
                                    user_tokens["access_token"]["token"]),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Missing attribute user_id"
    assert len(group.group_members) == 0
