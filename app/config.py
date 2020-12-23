import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret"

    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URI")
                               or "sqlite:///" +
                               os.environ.get("PWD") + "/sb.db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_ERROR_MESSAGE_KEY = "message"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


config = {
    "testing": TestingConfig,
    "default": Config
}
