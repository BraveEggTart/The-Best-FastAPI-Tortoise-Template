import redis

from app.config import settings


# 初始化 Redis 连接池
def get_redis():
    redis_pool = redis.ConnectionPool(
        host=settings.REDIS_URL,
        port=int(settings.REDIS_PORT),
        db=int(settings.REDIS_DB),
        password=settings.REDIS_PASSWORD,
        max_connections=50,
        decode_responses=True
    )
    r = redis.Redis(connection_pool=redis_pool)
    return r
