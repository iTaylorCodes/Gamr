import secrets

class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = secrets.token_hex(16)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
