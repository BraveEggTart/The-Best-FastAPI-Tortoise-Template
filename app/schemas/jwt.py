from typing import List, Optional

from pydantic import Field, EmailStr, BaseModel


class UserLoginSchema(BaseModel):
    account: str = Field(
        ...,
        description="账号/邮箱/手机号",
        examples=["admin"]
    )
    password: str = Field(
        ...,
        description="密码",
        examples=["123456"]
    )


class JWTOutSchema(BaseModel):
    name: str = Field(
        ...,
        description="昵称",
        examples=["admin"]
    )
    token: str = Field(
        ...,
        description="Token",
        examples=["a@test.org"]
    )
    roles: List[Optional[str]] = Field(
        ...,
        description="角色",
        examples=["SuperAdmin"]
    )
    expire: str = Field(
        ...,
        description="密码",
        examples=["123456"]
    )


class JWTPayloadSchema(BaseModel):
    id: int = Field(
        ...,
        gt=0,
        description="用户ID",
        examples=[1, ]
    )
    roles: List[Optional[int]] = Field(
        ...,
        description="角色列表",
        examples=[1, 2, 3, ]
    )
    is_superuser: bool = Field(
        False,
        description="超级管理员",
        examples=[False]
    )
    generate_time: str = Field(
        "",
        description="最后登录时间",
        examples=["2024-01-01 01:11:11"]
    )
    expire_time: str = Field(
        "",
        description="最后登录时间",
        examples=["2024-01-01 01:11:11"]
    )
