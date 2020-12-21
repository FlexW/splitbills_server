import json

from app.models.user import User, insert_user
from app.models.group import Group, insert_group
from app.models.group_member import GroupMember


def test_delete_user_from_existing_group(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password=password)
    user1 = insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    group_member1 = GroupMember(user=user1)
    group = Group(name="Muster",
                  group_members=[group_member1])
    insert_group(group)

    response = test_client.delete("/groups/{}/members/{}"
                                  .format(group.id, user1.id),
                                  headers=api_headers_bearer(
                                      user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Deleted user from group"
    assert group_member1.valid == 0


def test_dont_delete_user_if_user_not_in_group(test_client, api_headers_bearer, insert_tokens):
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

    group_member1 = GroupMember(user=user1)
    group = Group(name="Muster",
                  group_members=[group_member1])
    insert_group(group)

    response = test_client.delete("/groups/{}/members/{}"
                                  .format(group.id, user1.id),
                                  headers=api_headers_bearer(
                                      user2_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Group does not exist"
    assert group_member1.valid == 1


def test_dont_delete_user_if_not_in_group(test_client, api_headers_bearer, insert_tokens):
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

    response = test_client.delete("/groups/{}/members/{}"
                                  .format(group.id, user2.id),
                                  headers=api_headers_bearer(
                                      user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Group does not exist"
    assert group_member1.valid == 1
    assert len(group.group_members) == 1


def test_needs_to_be_authenticated_on_delete(test_client, api_headers):
    response = test_client.delete("/groups/1/members/1", headers=api_headers)
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Missing Authorization Header"
