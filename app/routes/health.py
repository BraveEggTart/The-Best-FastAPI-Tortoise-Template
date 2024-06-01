import logging

from fastapi import APIRouter

from app.schemas.response import Success

logger = logging.getLogger(__name__)
routes = APIRouter()


@routes.get(
    "/health",
    tags=["General"],
    summary="健康检查",
    description="用于监控服务运行状态",
    response_model=Success,
)
def health():
    logger.info("心跳检测正常")
    return Success()
