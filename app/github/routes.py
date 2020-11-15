import hmac

from flask import request, jsonify, current_app
from git import Repo
from . import github_blueprint


@github_blueprint.route("/github", methods=["POST"])
def github():
    """Entry point for github webhook."""

    signature = request.headers.get("X-Hub-Signature")
    sha, signature = signature.split("=")

    secret = str.encode(current_app.config.get("GITHUB_SECRET"))

    hashhex = hmac.new(secret, request.data, digestmod="sha1").hexdigest()
    if hmac.compare_digest(hashhex, signature):
        repo = Repo(current_app.config.get("REPO_PATH"))
        origin = repo.remotes.origin
        origin.pull("--rebase")

        commit = request.json["after"][0:6]
        print("Repository updated with commit {}".format(commit))

    return jsonify({}), 200
