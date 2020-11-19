import pytest

from app.models.user import User, insert_user, get_user_by_email, get_user_by_id

def test_password_setter():
    u = User(password="securepassword")

    assert u.password_hash is not None


def test_no_password_getter():
    u = User(password="securepassword")

    with pytest.raises(AttributeError):
        u.password


def test_password_verification():
    u = User(password="securepassword")

    assert u.verify_password("securepassword")
    assert not u.verify_password("unsecurepassword")


def test_password_salts_are_random():
    u1 = User(password="securepassword")
    u2 = User(password="securepassword")

    assert u1.password_hash is not u2.password_hash


def test_get_known_user_by_email(setup_app):
    u = User(first_name="Max",
             last_name="Muster",
             email="muster@mail.de",
             password="securepassword")

    insert_user(u)

    u_from_db = get_user_by_email(u.email)

    assert u == u_from_db


def test_dont_get_unknown_user_by_email(setup_app):
    u = User(first_name="Max",
             last_name="Muster",
             email="muster@mail.de",
             password="securepassword")

    insert_user(u)

    u_from_db = get_user_by_email("unmuster@mail.de")

    assert u_from_db is None


def test_get_known_user_by_id(setup_app):
    u = User(first_name="Max",
             last_name="Muster",
             email="muster@mail.de",
             password="securepassword")

    u = insert_user(u)

    u_from_db = get_user_by_id(u.id)

    assert u == u_from_db


def test_dont_get_unknown_user_by_id(setup_app):
    u = User(first_name="Max",
             last_name="Muster",
             email="muster@mail.de",
             password="securepassword")

    u = insert_user(u)

    u_from_db = get_user_by_id(0)

    assert u_from_db is None
