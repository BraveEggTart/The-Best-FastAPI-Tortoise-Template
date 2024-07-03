from tortoise import fields

from app.db.base import BaseModel


class Users(BaseModel):
    name = fields.CharField(
        max_length=20,
        description="昵称",
    )
    account = fields.CharField(
        max_length=30,
        description="账号",
        unique=True,
    )
    password = fields.CharField(
        max_length=100,
        description="密码",
    )

    class Meta:
        table = "users"
        table_description = "用户"
        ordering = ("-id", )
