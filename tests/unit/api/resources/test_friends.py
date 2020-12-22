import json

from app.models.friend import Friend
from app.models.user import User, insert_user


def test_get_friends(test_client, api_headers_bearer, insert_tokens):
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

    user1.friends.append(Friend(friend=user2))
    user1.friends.append(Friend(friend=user3))

    response = test_client.get("/friends",
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Returned friends"

    returned_friends = json_response["friends"]

    assert len(returned_friends) == 2
    assert returned_friends[0]["user_id"] == user2.id
    assert returned_friends[1]["user_id"] == user3.id


def test_get_only_friends_of_user(test_client, api_headers_bearer, insert_tokens):
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
    user2_tokens = insert_tokens(user2.email)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 password=password)
    insert_user(user3)

    user1.friends.append(Friend(friend=user2))
    user1.friends.append(Friend(friend=user3))

    user2.friends.append(Friend(friend=user1))

    response = test_client.get("/friends",
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    returned_friends = json_response["friends"]

    assert len(returned_friends) == 2
    assert returned_friends[0]["user_id"] == user2.id
    assert returned_friends[1]["user_id"] == user3.id

    response = test_client.get("/friends",
                               headers=api_headers_bearer(
                                   user2_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    returned_friends = json_response["friends"]

    assert len(returned_friends) == 1
    assert returned_friends[0]["user_id"] == user1.id
