from tortoise import fields

from app.models.base import BaseModel, TimestampMixin
from app.models.base import EnumBase


class ActionType(EnumBase):
    # 创建
    CREATE = "create"
    # 编辑
    UPDATE = "update"
    # 删除
    DELETE = "delete"
    # 登陆
    LOGIN = "login"
    # 注销
    LOGOUT = "logout"


class Operations(BaseModel, TimestampMixin):
    user_id = fields.ForeignKeyField("models.Users", description="操作人")
    action = fields.CharEnumField(ActionType, description="操作类型")
    operation = fields.CharField(max_length=20, description="操作内容")
    detail = fields.TextField(max_length=200, description="详细信息")

    class Meta:
        table = "operation"
        ordering = ("id", )
