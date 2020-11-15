from flask import Blueprint

github_blueprint = Blueprint("github_webhook", __name__, url_prefix="")

from . import routes
