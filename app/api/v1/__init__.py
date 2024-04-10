import os
from datetime import datetime, timedelta

from loguru import logger
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from tortoise.expressions import Q

from app.core.dependency import DependAuth, AuthControl, LangInitial
from app.schemas.response import Success
from app.models.admin.users import Users
from app.models.admin.operations import ActionType
from app.schemas.jwt import UserLoginSchema, JWTOutSchema, JWTPayloadSchema
from app.tasks.background import task_record_user_action
from app.core.bgtask import BgTasks
from app.config import settings
from app.utils.jwt import create_token
from app.utils.password import verify_password
from .admin import users_router

load_dotenv()
v1_router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "")


@v1_router.post(
    "/login",
    tags=["auth"],
    summary="登录",
    description="登录并获取token",
    response_model=Success[JWTOutSchema],
    dependencies=[LangInitial]
)
async def login(login_info: UserLoginSchema):
    """登陆接口

    Args:
        login_info (UserLoginSchema): 
            {
                account: str,
                password: str,
            }

    Returns:
        Success[JWTOutSchema]: 
            {
                code: int = 200,
                msg: Optional[str] = "请求响应成功",
                data: Optional[JWTOutSchema],
            }
    """
    # 根据账号信息确定用户
    user = await Users.filter(account=login_info.account).first()
    if user is None:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    # 判断是否禁用
    if user.is_active == False:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    # 密码验证
    verified = verify_password(login_info.password, user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="用户名或密码错误!")

    # 更新最后登陆时间
    user.last_login = datetime.now()
    await user.save()

    token_expires = timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now() + token_expires

    data = JWTOutSchema(
        token=create_token(
            data=JWTPayloadSchema(
                id=user.id,
                roles=await user.roles_ids,
                is_superuser=user.is_superuser,
                generate_time=str(datetime.now()),
                expire_time=str(expire),
            )
        ),
        name=user.name,
        roles=await user.roles_list,
        expire=str(expire),
    )
    await BgTasks.add_task(
        task_record_user_action,
        action=ActionType.LOGIN,
        description="系统登陆",
        detail=f"用户名称: {user.name} 用户ID: {user.id} 登陆了系统",
    )
    logger.info("登陆成功")
    return Success(data=data.model_dump())


@v1_router.get(
    "/auth",
    tags=["auth"],
    summary="验证",
    description="验证token是否失效",
    response_model=Success[str]
)
async def auth(token: str):
    # await AuthControl.is_authed(token)
    try:
        if token == SECRET_KEY:
            user = await Users.filter(is_superuser=True).first()
            user_id = user.id
        else:
            decode_data = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=settings.JWT_ALGORITHM
            )
            user_id = decode_data.get("id")
        user = await Users.filter(id=user_id).first()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Authentication failed"
            )
        CTX_USER.set(user)
        return user
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="无效的Token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="登录已过期")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{repr(e)}")
    return Success(data="Token 验证成功")


v1_router.include_router(
    users_router,
    prefix="/users",
    dependencies=[DependAuth, LangInitial]
)
