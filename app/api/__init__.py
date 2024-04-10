from fastapi import APIRouter

from .v1 import v1_router

api_router = APIRouter(
    responses={
        400: {
            "model": str,
        },
        401: {
            "model": str,
        },
        500: {
            "model": str,
        },
    }
)
api_router.include_router(v1_router, prefix="/v1")


__all__ = ["api_router"]
