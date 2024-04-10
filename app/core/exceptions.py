from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
    ResponseValidationError,
)
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError


class SettingNotFound(Exception):
    pass


class InstanceDoesNotExist(DoesNotExist):
    def __init__(self, model_name):
        super().__init__(f"{model_name} instance does not exist")


async def DoesNotExistHandle(
    req: Request,
    exc: DoesNotExist
) -> JSONResponse:
    content = dict(
        code=404,
        msg=f"""
        Object has not found, exc: {exc}, query_params: {req.query_params}
        """,
    )
    return JSONResponse(content=content, status_code=200)


async def IntegrityHandle(
    _: Request,
    exc: IntegrityError
) -> JSONResponse:
    content = dict(
        code=500,
        msg=f"IntegrityError，{exc}",
    )
    return JSONResponse(content=content, status_code=200)


async def HttpExcHandle(
    _: Request,
    exc: HTTPException
) -> JSONResponse:
    content = dict(code=exc.status_code, msg=exc.detail, data=None)
    return JSONResponse(content=content, status_code=200)


async def RequestValidationHandle(
    _: Request,
    exc: RequestValidationError
) -> JSONResponse:
    content = dict(code=422, msg=f"RequestValidationError, {exc}")
    return JSONResponse(content=content, status_code=200)


async def ResponseValidationHandle(
    _: Request,
    exc: ResponseValidationError
) -> JSONResponse:
    content = dict(code=500, msg=f"ResponseValidationError, {exc}")
    return JSONResponse(content=content, status_code=200)
