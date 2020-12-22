from app.models.user import User, insert_user
from app.models.friend import (Friend,
                               get_friends_by_user_id,
                               insert_friend,
                               is_friend_with_user)


def test_get_friends_by_user_id(app):
    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password="123")
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password="123")
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 password="123")
    insert_user(user3)

    friend1 = Friend(user=user1, friend=user2)
    insert_friend(friend1)

    friend2 = Friend(user=user1, friend=user3)
    insert_friend(friend2)

    friends_user1 = get_friends_by_user_id(user1.id)

    assert len(friends_user1) == 2
    assert friends_user1[0] == friend1
    assert friends_user1[1] == friend2


def test_get_friends_by_user_relationship(app):
    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password="123")
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password="123")
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 password="123")
    insert_user(user3)

    friend1 = Friend(user=user1, friend=user2)
    insert_friend(friend1)

    friend2 = Friend(user=user1, friend=user3)
    insert_friend(friend2)

    friends_user1 = user1.friends

    assert len(friends_user1) == 2
    assert friends_user1[0] == friend1
    assert friends_user1[1] == friend2


def test_insert_friends_by_user_relationship(app):
    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password="123")
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password="123")
    insert_user(user2)

    user3 = User(first_name="Max",
                 last_name="Muster",
                 email="muster3@mail.de",
                 password="123")
    insert_user(user3)

    user1.friends.append(Friend(friend=user2))
    user1.friends.append(Friend(friend=user3))

    friends_user1 = get_friends_by_user_id(user1.id)

    assert len(friends_user1) == 2
    assert friends_user1[0].friend_id == user2.id
    assert friends_user1[1].friend_id == user3.id


def test_is_friends_with_user_return_true_if_friend_with_user(app):
    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password="123")
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password="123")
    insert_user(user2)

    insert_friend(Friend(user=user1, friend=user2))

    result = is_friend_with_user(user1.id, user2.id)

    assert result is True


def test_is_friends_with_user_return_false_if_not_friend_with_user(app):
    user1 = User(first_name="Max",
                 last_name="Muster",
                 email="muster@mail.de",
                 password="123")
    insert_user(user1)

    user2 = User(first_name="Max",
                 last_name="Muster",
                 email="muster2@mail.de",
                 password="123")
    insert_user(user2)

    insert_friend(Friend(user=user1, friend=user2))

    result = is_friend_with_user(user2.id, user1.id)

    assert result is False
