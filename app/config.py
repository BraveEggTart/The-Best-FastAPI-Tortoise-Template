import os

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 项目信息配置
    TITLE: str = "Platform Backend"
    DESCRIPTION: str = "Platform Backend"
    VERSION: str = "0.1.0"

    # 跨域配置
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # JWT配置
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_MINUTES: int = 60 * 2

    # 项目路径设置
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(__file__))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))

    # 设定日期格式
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DATETIME_TIMEZONE: str = ""
    # openssl rand -hex 32
    SECRET_KEY: str = "32cf914b504263ba5a8983cc35e1ac905cc2dc976293ff12b0d968f0eb7c0fd8"
    PREFIX: str = "/api"

    # APScheduler 持久化存储
    TASKS_DB: str = "sqlite:///app/db/db.sqlite3"
    # TORTOISE 配置
    DB_URL: str = "sqlite://db.sqlite3"
    DB_FILE: str = os.path.join(PROJECT_ROOT, "app/db/") + "db.sqlite3"
    TORTOISE_ORM: dict = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.sqlite",
                "db_url": DB_URL,
                "credentials": {
                    "file_path": DB_FILE
                },
            }
        },
        "apps": {
            "models": {
                "models": ["app.common"],
                "default_connection": "default",
            },
        },
        "use_tz": False,
        "timezone": DATETIME_TIMEZONE,
    }

    class Config:
        env_file = ".env"

    # Redis 配置
    redisurl: str = ""
    REDIS_PORT: str = "6379"
    REDIS_DB: str = "0"
    redispass: str = ""

    DEBUGGER: bool = False


settings = Settings()
