import json

from app.models.user import User, insert_user
from app.models.group_member import GroupMember
from app.models.friend import get_friends_by_user_id
from app.models.group import Group, get_group_by_id, insert_group, get_all_groups


def test_add_group(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_data = {
        "name": "Muster",
        "members": [
            {
                "id": user.id,
            }
        ]
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201

    assert json_response["message"] == "Created new group"
    assert json_response["group"]["id"] == 1
    assert json_response["group"]["name"] == group_data["name"]
    assert json_response["group"]["valid"] is True

    group = get_group_by_id(json_response["group"]["id"])

    assert group is not None
    assert len(group.group_members) == 1


def test_get_groups_from_user(app, test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)

    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group1_member = GroupMember(user=user)

    group1 = Group(name="group1", group_members=[group1_member])
    insert_group(group1)

    group2_member = GroupMember(user=user)

    group2 = Group(name="group2", group_members=[group2_member])
    insert_group(group2)

    response = test_client.get("/groups",
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]))
    json_respone = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200

    assert json_respone["message"] == "Returned groups"

    assert len(json_respone["groups"]) == 2
    assert json_respone["groups"][0]["name"] == group1.name
    assert json_respone["groups"][1]["name"] == group2.name


def test_get_just_groups_from_user(app, test_client, api_headers_bearer, insert_tokens):
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
    user2_tokens = insert_tokens(user2.email)

    group1_member1 = GroupMember(user=user1)
    group1 = Group(name="group1",
                   group_members=[group1_member1])

    group2_member1 = GroupMember(user=user1)
    group2_member2 = GroupMember(user=user2)
    group2 = Group(name="group2",
                   group_members=[group2_member1, group2_member2])

    group3_member2 = GroupMember(user=user2)
    group3 = Group(name="group3",
                   group_members=[group3_member2])

    group1 = insert_group(group1)
    group2 = insert_group(group2)
    group3 = insert_group(group3)

    response = test_client.get("/groups",
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]))
    json_respone = json.loads(response.get_data(as_text=True))

    assert len(json_respone["groups"]) == 2
    assert json_respone["groups"][0]["name"] == group1.name
    assert json_respone["groups"][1]["name"] == group2.name

    response = test_client.get("/groups",
                               headers=api_headers_bearer(
                                   user2_tokens["access_token"]["token"]))
    json_respone = json.loads(response.get_data(as_text=True))

    assert len(json_respone["groups"]) == 2
    assert json_respone["groups"][0]["name"] == group2.name
    assert json_respone["groups"][1]["name"] == group3.name


def test_get_only_non_removed_groups(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    tokens = insert_tokens(user1.email)

    group1 = Group(name="G1", group_members=[GroupMember(user=user1)])
    insert_group(group1)
    group2 = Group(
        name="G1", group_members=[GroupMember(user=user1)], valid=False)
    insert_group(group2)

    response = test_client.get("/groups",
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]))
    json_respone = json.loads(response.get_data(as_text=True))

    assert len(json_respone["groups"]) == 1
    assert json_respone["groups"][0]["id"] == group1.id


def test_error_on_name_missing(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_data = {
        "members": [
            {
                "id": user.id,
            }
        ]
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Missing attribute name"

    assert len(get_all_groups()) == 0


def test_error_on_name_wrong_type(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_data = {
        "name": True,
        "members": [
            {
                "id": user.id,
            }
        ]
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Attribute name needs to be of type str"

    assert len(get_all_groups()) == 0


def test_error_on_members_missing(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_data = {
        "name": "Group"
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Missing attribute members"

    assert len(get_all_groups()) == 0


def test_error_on_members_wrong_type(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_data = {
        "name": "Group",
        "members": True
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Attribute members needs to be of type list"

    assert len(get_all_groups()) == 0


def test_error_on_wrong_member_id(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_data = {
        "name": "Muster",
        "members": [
            {
                "id": user.id,
            },
            {
                "id": 2,
            }
        ]
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400

    assert json_response["message"] == "User with id 2 does not exist"
    assert len(get_all_groups()) == 0


def test_error_on_user_not_in_group(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    insert_user(user1)
    tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)

    group_data = {
        "name": "Muster",
        "members": [
            {
                "id": user2.id,
            }
        ]
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400

    assert json_response["message"] == "User who created group must be group member"
    assert len(get_all_groups()) == 0


def test_insert_friends_of_user_after_adding_group(test_client, api_headers_bearer, insert_tokens):
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

    group_data = {
        "name": "Muster",
        "members": [
            {
                "id": user1.id,
            },
            {
                "id": user2.id,
            },
            {
                "id": user3.id,
            }

        ]
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(group_data))

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


def test_can_create_multiple_times_group_with_same_members(test_client, api_headers_bearer, insert_tokens):
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

    group_data = {
        "name": "Muster",
        "members": [
            {
                "id": user1.id,
            },
            {
                "id": user2.id,
            },
            {
                "id": user3.id,
            }

        ]
    }

    # Create group first time
    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(group_data))

    assert response.status_code == 201

    # Create group second time
    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    user1_tokens["access_token"]["token"]),
                                data=json.dumps(group_data))

    assert response.status_code == 201


def test_create_group_with_not_registered_group_member(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_data = {
        "name": "Muster",
        "members": [
            {
                "id": user.id,
            },
            {
                "email": "newuser@mail.de"
            }
        ]
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201

    assert json_response["message"] == "Created new group"
    assert json_response["group"]["id"] == 1
    assert json_response["group"]["name"] == group_data["name"]
    assert json_response["group"]["valid"] is True

    group = get_group_by_id(json_response["group"]["id"])

    assert group is not None
    assert len(group.group_members) == 2


def test_error_on_group_member_id_or_email_not_set(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    group_data = {
        "name": "Muster",
        "members": [
            {
                "id": user.id,
            },
            {
            }
        ]
    }

    response = test_client.post("/groups",
                                headers=api_headers_bearer(
                                    tokens["access_token"]["token"]),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Attribute id or email needs to be set"
    assert len(get_all_groups()) == 0
