import logging

from fastapi.middleware import Middleware
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.types import ASGIApp, Receive, Scope, Send
from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from apscheduler.triggers.interval import IntervalTrigger

from app.config import settings

logger = logging.getLogger(__name__)


class SchedulerMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        scheduler: AsyncScheduler,
    ) -> None:
        self.app = app
        self.scheduler = scheduler

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            logger.info("开始连接APScheduler数据库")
            async with self.scheduler:
                # await self.scheduler.add_schedule(
                #     schedule_function,
                #     IntervalTrigger(seconds=60),
                #     id="schedule_function_name",
                # )
                await scheduler.start_in_background()
                logger.info("定时器添加成功！")
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)


engine = create_async_engine(f"mysql+asyncmy://{settings.DB_URL}")
data_store = SQLAlchemyDataStore(engine)
scheduler = AsyncScheduler(data_store)
middleware = [Middleware(SchedulerMiddleware, scheduler=scheduler)]

APSchedulerMiddleware = Middleware(SchedulerMiddleware, scheduler=scheduler)
