from .env_vars import (
    DB_NAME,
    FLASK_ENV,
    MONGO_ADMIN,
    MONGO_HOST,
    MONGO_PASSWORD,
    MONGO_PORT,
    MONGO_USER,
)


class Config:
    """Base configuration."""

    DEBUG = False
    TESTING = False

    MONGO_HOST: str = MONGO_HOST
    MONGO_PORT: int = MONGO_PORT
    MONGO_USER: str = MONGO_USER
    MONGO_PASSWORD: str = MONGO_PASSWORD
    MONGO_ADMIN: str = MONGO_ADMIN
    DB_NAME: str = DB_NAME


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class TestingConfig(Config):
    """Testing configuration with separate test database."""

    DEBUG = True
    TESTING = True
    SERVER_NAME = "localhost:5000"
    DB_NAME: str = f"test_{DB_NAME}"
    REDIS_DB: int = 10


class ProductionConfig(Config):
    """Production configuration."""


def get_config() -> (
    type[DevelopmentConfig] | type[TestingConfig] | type[ProductionConfig]
):
    if FLASK_ENV == "development":
        return DevelopmentConfig
    elif FLASK_ENV == "testing":
        return TestingConfig
    else:
        return ProductionConfig
