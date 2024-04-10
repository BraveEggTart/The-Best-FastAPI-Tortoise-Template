from contextvars import ContextVar as ctxvar
from fastapi import BackgroundTasks as bgtasks
from app.models import Users

CTX_USER: ctxvar[Users] = ctxvar("user")
CTX_BG_TASKS: ctxvar[bgtasks] = ctxvar("bg_task", default=bgtasks())
CTX_LANG: ctxvar[str] = ctxvar("lang", default='zh')
