from app import auth
from app.models.user import get_user_by_email


@auth.verify_password
def verify_password(user_email, password):

    user = get_user_by_email(user_email)

    if user is None:
        return False

    return user.verify_password(password)
