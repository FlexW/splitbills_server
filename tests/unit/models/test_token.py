import pytest

from flask_jwt_extended import decode_token
from app.models.token import is_token_revoked, unrevoke_token, TokenNotFound


def test_is_token_revoked_error_on_token_not_found(app):
    token = {
        'iat': 1608567286,
        'nbf': 1608567286,
        'jti': '266cabc3-5b3c-4755-9095-d8d366ae8bf1',
        'exp': 1608568186,
        'identity': 'id',
        'fresh': False,
        'type': 'access',
        'user_claims': {}
    }

    assert is_token_revoked(token) is True


def test_unrevoke_token_error_on_token_not_found(app):

    with pytest.raises(TokenNotFound):
        unrevoke_token(1, "user")
