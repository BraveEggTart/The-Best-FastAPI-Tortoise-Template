import logging
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request
from redis import Redis

from app.config import settings
from app.db.redis import get_redis

logger = logging.getLogger(__name__)


def rate_limit(
    request: Request,
    redis_client: Redis = Depends(get_redis)
) -> None:
    minute = settings.RATE_LIMIT_MINUTES
    # 获取IP
    ip = request.state.ip
    ip_key = ip
    # 获取当前时间
    now = datetime.now()
    # 计算本周期剩余时间
    next_minute = (
        now + timedelta(minutes=minute)
    ).replace(second=0, microsecond=0)
    # 计算距离下一个整点时刻还有多久
    time_until_next_minute = (next_minute - now).seconds
    # 检查是否超过请求限制
    count = redis_client.get(ip_key)
    if count is not None:
        if int(count) >= settings.RATE_LIMIT:  # type: ignore
            raise HTTPException(
                status_code=429,
                detail="操作频繁, 请稍后再试"
            )
    else:
        # 设置键的失效时间
        redis_client.setex(
            ip_key,
            time_until_next_minute
            if time_until_next_minute > 0 else 60 * minute,
            0
        )
    # 更新请求次数
    redis_client.incr(ip_key)
