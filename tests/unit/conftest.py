import pytest

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from app import create_app
from app.models.token import add_token_to_database


@pytest.fixture
def app():
    app = create_app("testing")

    app_context = app.app_context()
    app_context.push()

    return app


@pytest.fixture
def test_client(app):
    return app.test_client()


@pytest.fixture
def api_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


@pytest.fixture
def api_headers_bearer():
    def _api_headers_bearer(token):
        return {
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    return _api_headers_bearer


@pytest.fixture
def insert_tokens():
    def _insert_tokens(identity):
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        access_token_id = add_token_to_database(
            access_token, current_app.config["JWT_IDENTITY_CLAIM"])
        refresh_token_id = add_token_to_database(
            refresh_token, current_app.config["JWT_IDENTITY_CLAIM"])

        result = {
            "access_token": {
                "id": access_token_id,
                "token": access_token
            },
            "refresh_token": {
                "id": refresh_token_id,
                "token": refresh_token
            }
        }

        return result
    return _insert_tokens
