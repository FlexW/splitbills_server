import json

from app.models.user import User, insert_user
from app.models.group import Group, get_group_by_id, insert_group


def test_add_group(app, test_client, api_headers_auth):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)

    group_data = {
        "name": "Muster",
        "members": [
            {
                "id": user.id,
            }
        ]
    }

    response = test_client.post("/groups",
                                headers=api_headers_auth(user.email, password),
                                data=json.dumps(group_data))
    json_response = json.loads(response.get_data(as_text=True))

    assert json_response["message"] == "Created new group."
    assert json_response["group"]["id"] == 1
    assert json_response["group"]["name"] == group_data["name"]

    group = get_group_by_id(json_response["group"]["id"])

    assert group is not None
    assert len(group.members) == 1


def test_get_groups_from_user(app, test_client, api_headers_auth):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)

    user = insert_user(user)

    group1 = Group(name="group1",
                  members=[user])
    group2 = Group(name="group2",
                   members=[user])

    group1 = insert_group(group1)
    group2 = insert_group(group2)

    response = test_client.get("/groups",
                               headers=api_headers_auth(user.email, password))
    json_respone = json.loads(response.get_data(as_text=True))

    assert len(json_respone["groups"]) == 2
    assert json_respone["groups"][0]["name"] == group1.name
    assert json_respone["groups"][1]["name"] == group2.name


def test_get_just_groups_from_user(app, test_client, api_headers_auth):
    password = "securepassword"

    user1 = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)

    user1 = insert_user(user1)
    user2 = insert_user(user2)

    group1 = Group(name="group1",
                  members=[user1])
    group2 = Group(name="group2",
                   members=[user1, user2])
    group3 = Group(name="group3",
                   members=[user2])

    group1 = insert_group(group1)
    group2 = insert_group(group2)
    group3 = insert_group(group3)

    response = test_client.get("/groups",
                               headers=api_headers_auth(user1.email, password))
    json_respone = json.loads(response.get_data(as_text=True))

    assert len(json_respone["groups"]) == 2
    assert json_respone["groups"][0]["name"] == group1.name
    assert json_respone["groups"][1]["name"] == group2.name

    response = test_client.get("/groups",
                               headers=api_headers_auth(user2.email, password))
    json_respone = json.loads(response.get_data(as_text=True))

    assert len(json_respone["groups"]) == 2
    assert json_respone["groups"][0]["name"] == group2.name
    assert json_respone["groups"][1]["name"] == group3.name
