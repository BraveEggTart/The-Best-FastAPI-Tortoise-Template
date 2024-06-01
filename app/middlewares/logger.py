import logging

from starlette.requests import Request

from .base import BaseMiddleware


logger = logging.getLogger(__name__)


class LoggerMiddleware(BaseMiddleware):

    async def before_request(self, request: Request):

        logger.info(f"""
            IP: {getattr(request.client, "host", "No IP Address")}\n
            METHOD: {request.method}\n
            PATH:{request.url.path}\n
            HEADERS: {request.headers}\n
        """)
