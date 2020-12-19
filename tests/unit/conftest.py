import pytest

from base64 import b64encode
from app import create_app
from app.models.user import User, insert_user


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
def api_headers_auth():
    def _api_headers_auth(user, password):
        return {
            "Authorization": "Basic " + b64encode(
                (user + ":" + password).encode("utf-8")).decode("utf-8"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    return _api_headers_auth


@pytest.fixture
def api_headers_bearer():
    def _api_headers_bearer(token):
        return {
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    return _api_headers_bearer
