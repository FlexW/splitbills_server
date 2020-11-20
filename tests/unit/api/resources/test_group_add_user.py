import json

from app.models.user import User, insert_user, get_all_users
from app.models.group import Group, insert_group, get_group_by_id, get_all_groups
from app.models.group_member import GroupMember


def test_add_user_to_existing_group(app, test_client, api_headers_auth):
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

    group_add_user_data = {
        "user_id": user2.id,
        "group_id": group.id
    }

    response = test_client.post("/groups/add_user",
                                headers=api_headers_auth(user1.email, password),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Added user to group."

    group = get_group_by_id(group.id)

    assert len(group.group_members) == 2


def test_dont_add_user_if_group_not_exist(test_client, api_headers_auth):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)

    group_add_user_data = {
        "user_id": user.id,
        "group_id": 1
    }

    response = test_client.post("/groups/add_user",
                                headers=api_headers_auth(user.email, password),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Group does not exist."
    assert len(get_all_groups()) == 0


def test_dont_add_user_if_user_not_exist(test_client, api_headers_auth):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)

    group_member = GroupMember(user=user)
    group = Group(name="Group",
                  group_members=[group_member])
    insert_group(group)

    group_add_user_data = {
        "user_id": 2,
        "group_id": group.id
    }

    response = test_client.post("/groups/add_user",
                                headers=api_headers_auth(user.email, password),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "User does not exist."
    assert len(get_all_users()) == 1


def test_dont_add_user_if_user_already_in_group(test_client, api_headers_auth):
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
    group_member2 = GroupMember(user=user2)
    group = Group(name="Group",
                  group_members=[group_member1, group_member2])
    insert_group(group)

    group_add_user_data = {
        "user_id": user2.id,
        "group_id": group.id
    }

    response = test_client.post("/groups/add_user",
                                headers=api_headers_auth(user1.email, password),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "User is already in group."
    assert len(group.group_members) == 2


def test_dont_add_user_if_user_not_in_group(test_client, api_headers_auth):
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
        "group_id": group.id
    }

    response = test_client.post("/groups/add_user",
                                headers=api_headers_auth(user2.email, password),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Forbidden"
    assert len(group.group_members) == 1


def test_dont_add_user_if_user_id_missing(test_client, api_headers_auth):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)

    group = Group(name="Group")
    insert_group(group)

    group_add_user_data = {
        "group_id": group.id
    }

    response = test_client.post("/groups/add_user",
                                headers=api_headers_auth(user.email, password),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Could not find all required fields."
    assert len(group.group_members) == 0


def test_dont_add_user_if_group_id_missing(test_client, api_headers_auth):
    password = "securepassword"

    user1 = User(first_name="Max",
                last_name="Muster",
                email="muster1@mail.de",
                password=password)
    insert_user(user1)
    user2 = User(first_name="Max",
                last_name="Muster",
                email="muster2@mail.de",
                password=password)
    insert_user(user2)

    group_member1 = GroupMember(user=user1)
    group = Group(name="Group",
                  group_members=[group_member1])
    insert_group(group)

    group_add_user_data = {
        "user_id": user2.id
    }

    response = test_client.post("/groups/add_user",
                                headers=api_headers_auth(user1.email, password),
                                data=json.dumps(group_add_user_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Could not find all required fields."
    assert len(group.group_members) == 1
