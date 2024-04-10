from typing import List, Optional
from pydantic import Field, EmailStr, BaseModel


class UserCreateSchema(BaseModel):
    name: Optional[str] = Field(
        "默认昵称", description="昵称", examples=["Admin"])
    account: str = Field(
        ..., description="账号", examples=["admin"])
    email: Optional[EmailStr] = Field(
        ...,  description="邮箱", examples=["a@test.org"])
    phone: Optional[str] = Field(
        "",  description="电话", examples=[13111111111])
    password: str = Field(
        ...,  description="密码", examples=["123456"])
    avatar: Optional[str] = Field(
        "",  description="头像", examples=["13111111111"])
    is_superuser: Optional[bool] = Field(
        False, description="超级管理员", examples=[False])


class UserUpdateSchema(BaseModel):
    id: int = Field(..., gt=0, description="ID", examples=[1, ])
    name: Optional[str] = Field(None, description="昵称", examples=["admin"])
    email: EmailStr = Field("",  description="邮箱", examples=["a@test.org"])
    phone: int = Field("",  description="用户名", examples=["13111111111"])
    avatar: str = Field("",  description="头像", examples=["13111111111"])
    is_superuser: bool = Field(False, description="超级管理员", examples=[False])
    roles: List[int] = Field([], description="角色", examples=[1, 2, 3])


class UpdatePasswordSchema(BaseModel):
    id: int = Field(..., gt=0, description="ID", examples=[1, ])
    old_password: str = Field(...,  description="旧密码", examples=["123456"])
    new_password: str = Field(...,  description="新密码", examples=["654321"])


class UserResponseSchema(BaseModel):
    id: int = Field(..., description="ID", examples=[1])
    name: str = Field(..., description="昵称", examples=["Admin"])
    account: str = Field(..., description="账号", examples=["admin"])
    email: str = Field(..., description="邮箱", examples=["example@test.com"])
    avatar: str = Field(..., description="头像", examples=["Admin"])
    phone: str = Field(..., description="电话", examples=["12345678901"])
    roles: List[Optional[str]] = Field(..., description="角色", examples=[["超级管理员"]])

    is_active: bool = Field(
        True, description="是否激活", examples=[True])
    is_superuser: bool = Field(
        True, description="是否为超级用户", examples=[False])
    created_at: str = Field(
        ..., description="创建时间", examples=["2024-04-07 10:58:39"])
    updated_at: str = Field(
        ..., description="更新时间", examples=["2024-04-07 10:58:39"])
    last_login: Optional[str] = Field(
        None, description="最后登陆时间", examples=["2024-04-07 10:58:39"])

