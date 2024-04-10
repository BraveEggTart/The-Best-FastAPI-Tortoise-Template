import os

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 项目信息配置
    NAME: str = "FastAPI Tortoise Template"
    TITLE: str = "FastAPI Tortoise Template"
    DESCRIPTION: str = "The Best FastAPI Tortoise Template"
    VERSION: str = "0.1.0"

    # 跨域配置
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # 启动模式配置
    DEBUG: bool = True

    # JWT配置
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 day

    # 项目路径设置
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(__file__))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(PROJECT_ROOT, "logs")

    # 是否生成日志文件
    LOG: bool = False
    DATETIME_FORMAT: str = ""
    # openssl rand -hex 32
    SECRET_KEY: str = ""
    DATETIME_TIMEZONE: str = ""

    # APScheduler 持久化存储
    TASKS_DB: str = ""
    # TORTOISE 配置
    DB_URL: str = ""
    DB_FILE: str = os.path.join(PROJECT_ROOT, "db/") + "db.sqlite3"
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
                "models": ["app.models", "aerich.models"],
                "default_connection": "default",
            },
        },
        "use_tz": False,
        "timezone": DATETIME_TIMEZONE,
    }

    class Config:
        env_file = ".env"


settings = Settings()
