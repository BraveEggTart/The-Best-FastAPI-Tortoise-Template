import re
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi_pagination import add_pagination
from tortoise.contrib.fastapi import RegisterTortoise

from app.config import settings
from app.db import init_db
from app.exceptions import register_exceptions
from app.middlewares import make_middlewares
from app.routes import register_routers

# 设置日志Level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TORTOISE_ORM = {
    "connections": {
        "default": f"mysql://{settings.DB_URL}",
    },
    "apps": {
        "models": {
            "models": ["app.common"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": settings.DATETIME_TIMEZONE,
}


def custom_generate_unique_id(route: APIRoute) -> str:
    """openapi operationID 命名规则转变
    由接口路由函数名 下划线转大驼峰小驼峰
    """
    operation_id = re.sub(
        '_([a-zA-Z])',
        lambda m: (m.group(1).upper()),
        route.name.lower()
    )
    return operation_id


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    async with RegisterTortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
    ):
        # db connected

        # init data
        await init_db()

        yield

        # app teardown

    # db connections closed


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        openapi_url="/openapi.json",
        middleware=make_middlewares(),
        generate_unique_id_function=custom_generate_unique_id,
        lifespan=lifespan,
    )

    # register routes
    register_routers(app=app, prefix=settings.PREFIX)

    # register exception handler
    register_exceptions(app=app)

    # register pagination
    add_pagination(app)

    return app


app = create_app()
