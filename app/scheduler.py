from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from app.config import settings
from app.common.schedules import task_test

# 初始化APScheduler
jobstores = {
    'default': SQLAlchemyJobStore(url=settings.TASKS_DB)
}

scheduler = AsyncIOScheduler(jobstores=jobstores)


scheduler.add_job(
    task_test,
    'interval',
    seconds=5,
)
