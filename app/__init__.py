from flask import Flask
from .config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_blueprints(app)
    return app


def register_blueprints(app):
    from app.content import content_blueprint

    app.register_blueprint(content_blueprint)
