from flask_jwt_extended import get_jwt_identity
from app.models.user import get_user_by_email


def get_authorized_user():
    authorized_user_email = get_jwt_identity()
    authorized_user = get_user_by_email(authorized_user_email)

    return authorized_user
