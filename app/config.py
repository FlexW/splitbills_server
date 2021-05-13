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

    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = os.environ.get("MAIL_PORT") or 25
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or None
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or None
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") == "True"
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") == "True"

    MAIL_SUBJECT_PREFIX = "[SplitBills]"
    MAIL_SENDER = "SplitBills Admin <admin@splitbills.org>"

    ACCOUNT_CONFIRMATION = os.environ.get("ACCOUNT_CONFIRMATION") == "True"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


config = {
    "testing": TestingConfig,
    "default": Config
}
