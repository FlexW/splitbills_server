from app import jwt
from app.models.token import is_token_revoked


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)
