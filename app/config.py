import os

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Infomation
    TITLE: str = "Platform Backend"
    DESCRIPTION: str = "Platform Backend"
    VERSION: str = "0.1.0"

    # CORS
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_MINUTES: int = 60 * 2

    # project path
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(__file__))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))

    # datetime format
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DATETIME_TIMEZONE: str = "Asia/Shanghai"
    # openssl rand -hex 32
    SECRET_KEY: str = ""
    PREFIX: str = "/api"

    # Database
    DB_URL: str = ""
    # REDIS
    REDIS_URL: str = ""
    REDIS_PORT: str = ""
    REDIS_DB: str = ""
    REDIS_PASSWORD: str = ""

    # Rate limit per minute
    RATE_LIMIT_MINUTES: int = 100

    # Mail Config
    MAIL_USER: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 0
    MAIL_SERVER: str = ""

    DEBUGGER: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
