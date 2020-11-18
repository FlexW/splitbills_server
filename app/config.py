import os


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.environ.get("PWD") + "/sb.db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


config = {
    "testing": TestingConfig,
    "default": Config
}
