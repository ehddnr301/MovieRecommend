import os

from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    ENV: str = os.getenv("ENV")

class DevelopmentConfig(BaseConfig):
    DB_URL: str = os.getenv("TEST_DATABASE_URL")


class ProductionConfig(BaseConfig):
    DB_URL: str = os.getenv("PROD_DATABASE_URL")


def get_config():
    config_dict = {"development": DevelopmentConfig, "production": ProductionConfig}

    return config_dict[os.getenv("ENV")]


Config = get_config()
