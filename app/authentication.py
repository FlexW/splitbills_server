from flask import g
from app import auth
from app.models.user import get_user_by_email


@auth.verify_password
def verify_password(user_email, password):

    user = get_user_by_email(user_email)

    if user is None:
        return False

    g.current_user = user

    return user.verify_password(password)
