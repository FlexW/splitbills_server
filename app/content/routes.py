from flask import render_template
from . import content_blueprint


@content_blueprint.route('/')
def index():
    return render_template("index.html")
