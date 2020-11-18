import pytest

from app import create_app

@pytest.fixture
def setup_app():
    app = create_app("testing")

    app_context = app.app_context()
    app_context.push()

    return app
