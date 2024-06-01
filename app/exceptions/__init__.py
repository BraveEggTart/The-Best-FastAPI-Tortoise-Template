from fastapi import FastAPI, Request
from jwt import DecodeError, ExpiredSignatureError

from app.schemas.response import Fail


def register_exceptions(app: FastAPI):

    @app.exception_handler(DecodeError)
    async def decode_handle(
        _: Request,
        exc: DecodeError
    ) -> Fail:
        return Fail(code=401, msg=str(exc))

    async def expiredsignature_handle(
        _: Request,
        exc: ExpiredSignatureError
    ) -> Fail:
        return Fail(code=401, msg=str(exc))
