from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from .config import config

auth = HTTPBasicAuth()
db = SQLAlchemy()
jwt = JWTManager()

# Import to get registered
from app.authentication import verify_password


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    jwt.init_app(app)

    register_api(app)

    # Important to init db at last, since models need to be imported
    # first
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


def register_api(app):
    from flask_restful import Api
    from app.api import init_routes

    api = Api(app)
    init_routes(api)
