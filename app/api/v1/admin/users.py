import logging
from typing import Optional, List

from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate
from tortoise.expressions import Q

from app.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UpdatePasswordSchema
)
from app.core.dependency import DependPermisson
from app.schemas.response import Success, Success, Fail
from app.schemas.users import UserResponseSchema
from app.models.admin.users import Users
from app.core.ctx import CTX_USER
from app.utils.password import get_password_hash, verify_password

logger = logging.getLogger(__name__)

users_router = APIRouter()


@users_router.get(
    "/list",
    summary="查看用户列表",
    description="根据页面大小及页码数获取用户列表",
    tags=["system"],
    dependencies=[DependPermisson],
    response_model=Success[List[UserResponseSchema]]
)
async def list_user(
    name: Optional[str] = Query(None, description="昵称", examples=["Admin"]),
    account: Optional[str] = Query(None, description="账号", examples=["admin"]),
    email: Optional[str] = Query(
        None, description="邮箱", examples=["example@test.com"]),
    phone: Optional[str] = Query(
        None, description="电话", examples=["12345678901"]),
    is_active: Optional[bool] = Query(
        True, description="是否激活", examples=[True]),
    page: int = Query(1, description="当前页码", examples=[1]),
    size: int = Query(20, description="每页记录数量", examples=[20]),
):
    filter_conditions = {
        "name__icontains": name,
        "account__icontains": account,
        "email__icontains": email,
        "phone__icontains": phone,
        "is_active": is_active
    }
    q = Q()
    for key, value in filter_conditions.items():
        if value is not None:
            q &= Q(**{key: value})
    data = await paginate(
        Users.filter(q),
        params=Params(page=page, size=size)
    )
    result = [
        await item.to_dict(exclude=("password", ), m2m=True)
        for item in data.items
    ]
    return Success(
        data=result,
        total=data.total,
        page=data.page,
        size=data.size,
        pages=data.pages
    )
