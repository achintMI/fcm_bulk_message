import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ENV = ""
    BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    BACKEND_URL = os.environ.get("CELERY_BACKEND_URL")
    TEMP_FILES_DIR = "tempFiles"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "dev"


class TestingConfig(Config):
    ENV = "test"


class ProductionConfig(Config):
    ENV = "prod"


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
