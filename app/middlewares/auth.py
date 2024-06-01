import logging

import jwt
from starlette.requests import Request
from starlette.types import Scope, Receive

from app.config import settings
from .base import BaseMiddleware

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):

    async def before_request(self, request: Request):

        # token = request.headers.get(
        #     "Authorization",
        #     "Bearer "
        # ).replace("Bearer ", "")
        # payload = jwt.decode(
        #     token,
        #     settings.SECRET_KEY,
        #     algorithms=[settings.JWT_ALGORITHM]
        # )
        # request.state.user_id = payload['user_id']
        # request.state.role = payload['role']
        request.state.role = "test"
