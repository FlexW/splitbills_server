class Config:
    pass


class TestingConfig(Config):
    TESTING = True


config = {
    "testing": TestingConfig,
    "default": Config
}
