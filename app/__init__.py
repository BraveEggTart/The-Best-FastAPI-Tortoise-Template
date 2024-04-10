import re
from types import ModuleType
from typing import Optional, Dict, Union, Iterable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from loguru import logger
from tortoise import Tortoise
from tortoise.connection import connections
from fastapi_pagination import add_pagination

from app.core.scheduler import scheduler
from app.core import monkey_patches

from app.core.init_app import (
    register_routers,
    register_page,
    register_exceptions,
    register_hook,
    make_middlewares,
    register_static_file,
    init_db,
)
from app.config import settings

TORTOISE_ORM = settings.TORTOISE_ORM


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

    # 注册路由
    register_routers(app, prefix="/api")

    # 注册分页
    register_page(app)

    # 注册捕获全局异常
    register_exceptions(app)

    # 请求拦截
    register_hook(app)

    if settings.DEBUG:
        # 注册静态文件
        register_static_file(app)
    return app


def register_tortoise(
    config: Optional[dict] = None,
    config_file: Optional[str] = None,
    db_url: Optional[str] = None,
    modules: Optional[Dict[str, Iterable[Union[str, ModuleType]]]] = None,
    generate_schemas: bool = False,
) -> AbstractAsyncContextManager:
    async def init_orm() -> None:  # pylint: disable=W0612
        await Tortoise.init(config=config, config_file=config_file, db_url=db_url, modules=modules)
        logger.info("Tortoise-ORM started")
        if generate_schemas:
            logger.info("Tortoise-ORM generating schema")
            await Tortoise.generate_schemas()

    async def close_orm() -> None:  # pylint: disable=W0612
        await connections.close_all()
        logger.info("Tortoise-ORM shutdown")

    class Manager(AbstractAsyncContextManager):
        async def __aenter__(self) -> "Manager":
            await init_orm()
            return self

        async def __aexit__(self, *args, **kwargs) -> None:
            await close_orm()


    return Manager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 连接数据库
    async with register_tortoise(
        config=settings.TORTOISE_ORM,
        generate_schemas=True,
    ):
        # 开始定时任务
        scheduler.start()
        # 初始化数据库
        await init_db()
        yield


app = create_app()
