import json

from app.models.user import User, insert_user


def test_confirm_user(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    confirm_token = user.generate_confirmation_token()

    response = test_client.put("/users/confirm/{}".format(confirm_token),
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert json_response["message"] == "Account confirmed"
    assert user.confirmed is True


def test_user_already_confirmed(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password,
                confirmed=True)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    confirm_token = user.generate_confirmation_token()

    response = test_client.put("/users/confirm/{}".format(confirm_token),
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_response["message"] == "Account already confirmed"
    assert user.confirmed is True


def test_confirm_token_invalid(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user = User(first_name="Max",
                last_name="Muster",
                email="muster@mail.de",
                password=password)
    user = insert_user(user)
    tokens = insert_tokens(user.email)

    response = test_client.put("/users/confirm/abc",
                               headers=api_headers_bearer(
                                   tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Confirmation token invalid"
    assert user.confirmed is False


def test_dont_confirm_if_token_from_other_user(test_client, api_headers_bearer, insert_tokens):
    password = "securepassword"

    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster1@mail.de",
                 password=password)
    insert_user(user1)
    user1_tokens = insert_tokens(user1.email)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password=password)
    insert_user(user2)
    user2_confirm_token = user2.generate_confirmation_token()

    response = test_client.put("/users/confirm/{}".format(user2_confirm_token),
                               headers=api_headers_bearer(
                                   user1_tokens["access_token"]["token"]))
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert json_response["message"] == "Confirmation token invalid"
    assert user1.confirmed is False
    assert user2.confirmed is False


def test_needs_to_be_authenticated_on_put(test_client, api_headers):
    response = test_client.put("/users/confirm/abc", headers=api_headers)
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_response["message"] == "Missing Authorization Header"
