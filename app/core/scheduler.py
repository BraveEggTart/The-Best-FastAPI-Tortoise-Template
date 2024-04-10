from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from app.config import settings

# 初始化APScheduler
jobstores = {
    'default': SQLAlchemyJobStore(url=settings.TASKS_DB)
}

scheduler = AsyncIOScheduler(jobstores=jobstores)
