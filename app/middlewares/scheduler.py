from datetime import datetime

from fastapi.middleware import Middleware
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.types import ASGIApp, Receive, Scope, Send
from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from apscheduler.triggers.interval import IntervalTrigger

from app.config import settings


def tick():
    print("Hello, the time is", datetime.now())


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
            async with self.scheduler:
                await self.scheduler.add_schedule(
                    tick, IntervalTrigger(seconds=1), id="tick"
                )
                await scheduler.start_in_background()
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)


engine = create_async_engine(f"mysql+asyncmy://{settings.DB_URL}")
data_store = SQLAlchemyDataStore(engine)
scheduler = AsyncScheduler(data_store)
middleware = [Middleware(SchedulerMiddleware, scheduler=scheduler)]

APSchedulerMiddleware = Middleware(SchedulerMiddleware, scheduler=scheduler)
