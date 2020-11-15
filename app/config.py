import os


class Config:
    GITHUB_SECRET = os.environ.get("GITHUB_SECRET") or "github_secret"
    REPO_PATH = os.environ.get("REPO_PATH") or "repo_path"


class TestingConfig(Config):
    TESTING = True


config = {
    "testing": TestingConfig,
    "default": Config
}
