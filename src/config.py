import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = b'\xfe/0\xb1\xa0VV\x9a\xda\xc6O\xc6_\xec\xe2\x9b'
    TESTING = False
    DEBUG = False
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass


config_modes = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}