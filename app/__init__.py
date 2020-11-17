from flask import Flask
from .config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_api(app)

    return app


def register_api(app):
    from flask_restful import Api
    from app.api import init_routes

    api = Api(app)
    init_routes(api)
