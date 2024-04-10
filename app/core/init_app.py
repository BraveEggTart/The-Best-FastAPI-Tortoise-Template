import os
from typing import List

from fastapi import FastAPI, Request, Response
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from .middlewares import BackGroundTaskMiddleware
from app.log import logger
# from app.tasks.schedules import task_test
from app.api import api_router
from app.core.exceptions import (
    DoesNotExist,
    DoesNotExistHandle,
    HTTPException,
    HttpExcHandle,
    IntegrityError,
    IntegrityHandle,
    RequestValidationError,
    RequestValidationHandle,
    ResponseValidationError,
    ResponseValidationHandle,
)
from app.config import settings
from initialiazation.initial_database import (
    init_superuser,
    init_apis,
)


async def init_db():
    """
    生成初始数据
    :param:
    :return:
    """
    await init_apis()
    await init_superuser()


def register_routers(app: FastAPI, prefix: str = "/api") -> None:
    """
    注册路由
    :param app:
    :return:
    """
    # 项目API
    app.include_router(api_router, prefix=prefix)


def register_page(app: FastAPI) -> None:
    """
    分页查询

    :param app:
    :return:
    """
    add_pagination(app)


def register_exceptions(app: FastAPI) -> None:
    """
    异常捕获
    :param app:
    :return:
    """
    app.add_exception_handler(DoesNotExist, DoesNotExistHandle)
    app.add_exception_handler(HTTPException, HttpExcHandle)
    app.add_exception_handler(IntegrityError, IntegrityHandle)
    app.add_exception_handler(RequestValidationError, RequestValidationHandle)
    app.add_exception_handler(
        ResponseValidationError,
        ResponseValidationHandle
    )


def register_hook(app: FastAPI) -> None:
    """
    请求响应拦截 hook
    :param app: FastAPI
    :return:
    """

    @app.middleware("http")
    async def logger_request(request: Request, call_next) -> Response:
        logger.info(f"""
                    IP:{request.client.host}\n
                    headers:{request.headers}\n
                    访问记录:{request.method} url:{request.url}\n
                    """)
        response = await call_next(request)
        return response


def make_middlewares() -> List[Middleware]:
    """
    设置中间件：跨域，后台任务
    :param app: FastAPI
    :return: List[Middleware]
    """
    middleware = [
        # 跨域中间件
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
        ),
        # 后台任务中间件
        Middleware(BackGroundTaskMiddleware),
    ]
    return middleware


def register_static_file(app: FastAPI) -> None:
    """
    静态文件交互开发模式使用
    生产使用 nginx 静态资源服务
    这里是开发是方便本地
    :param app:
    :return:
    """
    static_dir = ["./static", "./db", "./logs"]
    map(os.mkdir, static_dir)
    app.mount("/static", StaticFiles(directory="static"), name="static")
