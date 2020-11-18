from app.models.user import User, insert_user
from app.auth import verify_password

def test_verify_correct_password(setup_app):
    password="securepassword"
    u = User(first_name="Max",
             last_name="Muster",
             email="muster@mail.de",
             password=password)

    insert_user(u)

    assert verify_password(u.email, password)


def test_dont_verify_incorrect_password(setup_app):
    u = User(first_name="Max",
             last_name="Muster",
             email="muster@mail.de",
             password="securepassword")

    insert_user(u)

    assert not verify_password(u.email, "incorrect")
