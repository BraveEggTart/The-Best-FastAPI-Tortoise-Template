import logging

from fastapi import APIRouter, FastAPI

from app.routes.health import routes as health_routes
from app.common.routes import router as common_routes
from app.routes.main import routes as mail_routes

logger = logging.getLogger(__name__)
api_router = APIRouter(
    responses={
        400: {
            "model": str,
            "description": "test description",
        },
        401: {
            "model": str,
            "description": "test description",
        },
        500: {
            "model": str,
            "description": "test description",
        },
    }
)

api_router.include_router(
    health_routes,
)
api_router.include_router(
    common_routes
)
api_router.include_router(
    mail_routes
)


def register_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)
