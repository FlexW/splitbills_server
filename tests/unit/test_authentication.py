from flask import g
from app.models.user import User, insert_user
from app.authentication import verify_password

def test_verify_correct_password(app):
    password="securepassword"
    u = User(first_name="Max",
             last_name="Muster",
             email="muster@mail.de",
             password=password)

    insert_user(u)

    assert verify_password(u.email, password)
    assert g.current_user == u


def test_dont_verify_incorrect_password(app):
    u = User(first_name="Max",
             last_name="Muster",
             email="muster@mail.de",
             password="securepassword")

    insert_user(u)

    assert not verify_password(u.email, "incorrect")
