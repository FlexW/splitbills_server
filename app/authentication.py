from flask import g
from app import auth, jwt
from app.models.user import get_user_by_email
from app.models.token import is_token_revoked


@auth.verify_password
def verify_password(user_email, password):

    user = get_user_by_email(user_email)

    if user is None:
        return False

    g.current_user = user

    return user.verify_password(password)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)
