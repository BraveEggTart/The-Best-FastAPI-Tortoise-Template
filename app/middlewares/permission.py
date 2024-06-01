import logging

from starlette.requests import Request

from .base import BaseMiddleware

logger = logging.getLogger(__name__)


class PermissionMiddleware(BaseMiddleware):

    async def before_request(self, request: Request):
        ...
