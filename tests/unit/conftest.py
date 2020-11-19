import pytest

from app import create_app


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
