import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from tortoise.contrib.fastapi import RegisterTortoise

from app.config import settings
from app.db import init_db
from app.exceptions import register_exceptions
from app.middlewares import make_middlewares
from app.routes import register_routers
from app.scheduler import scheduler

# 设置日志Level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    async with RegisterTortoise(
        app,
        config=settings.TORTOISE_ORM,
        generate_schemas=True,
    ):
        # db connected

        # start scheduler
        scheduler.start()

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
