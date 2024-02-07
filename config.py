# config.py


class Config(object):
    # General configuration settings
    SECRET_KEY = 'user123'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///daniel'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # ... (other configuration settings)

class TestConfig(Config):
    # Test-specific configuration settings
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///test_blogly'
    DEBUG_TB_ENABLED = False
    # ... (other test configuration settings)

