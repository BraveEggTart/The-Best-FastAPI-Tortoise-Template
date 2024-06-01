import logging

from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Receive, Send

logger = logging.getLogger(__name__)


class BaseMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # make a request object
        request = Request(scope, receive=receive)

        # pre hook
        await self.before_request(request)
        # execute
        await self.app(request.scope, request.receive, send)
        # post hook
        await self.after_response(request)

    async def before_request(self, request: Request) -> None:
        ...

    async def after_response(self, request: Request) -> None:
        ...
