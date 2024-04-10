from datetime import datetime
from collections import defaultdict
from typing import Union, List, Tuple, Optional

from tortoise import fields

from app.models.base import BaseModel, TimestampMixin
from app.config import settings


class Users(BaseModel, TimestampMixin):
    name = fields.CharField(
        max_length=20,
        description="昵称",
    )
    account = fields.CharField(
        max_length=30,
        description="账号",
        unique=True,
    )

    email = fields.CharField(
        max_length=255,
        description="电子邮件地址",
        null=True,
    )
    captcha = fields.CharField(
        max_length=8,
        description="邮箱验证码",
        null=True,
    )
    email_expire = fields.DatetimeField(
        max_length=8,
        description="邮箱验证码过期时间",
        null=True,
    )

    phone = fields.CharField(
        max_length=20,
        description="联系电话",
        null=True,
    )
    sms_captcha = fields.CharField(
        max_length=8,
        description="短信验证码",
        null=True,
    )
    sms_expire = fields.DatetimeField(
        max_length=8,
        description="短信验证码过期时间",
        null=True,
    )

    avatar = fields.CharField(
        max_length=100,
        description="头像",
        null=True,
    )

    password = fields.CharField(
        max_length=100,
        description="密码",
    )
    is_active = fields.BooleanField(
        description="是否激活",
        null=True,
    )

    is_superuser = fields.BooleanField(
        description="是否为超级管理员",
        default=False,
    )
    last_login = fields.DatetimeField(
        description="最后登录时间",
        null=True,
    )
    multi_device = fields.BooleanField(
        description="是否开启多设备登陆",
        default=False,
    )
    roles = fields.ManyToManyField(
        "models.Roles",
        related_name="users"
    )

    class Meta:
        table = "users"
        table_description = "用户"
        ordering = ("last_login", )

    async def to_dict(
        self,
        exclude: Union[List, Tuple] = [],
        m2m: bool = False,
    ):
        result = {}
        curr_exclude = []
        relation_exclude = defaultdict(list)
        for item in exclude:
            if '__' in item:
                field, name = item.split("__", 1)
                relation_exclude[field].append(name)
            else:
                curr_exclude.append(item)
        remain_field = self._meta.db_fields.difference(set(curr_exclude))
        for field in remain_field:
            value = getattr(self, field)
            if isinstance(value, datetime):
                value = value.strftime(settings.DATETIME_FORMAT)
            result[field] = value
        if m2m:
            for field in self._meta.m2m_fields:
                values = await getattr(self, field).all().values_list(
                    "name", flat=True
                )
                result[field] = values
        return result

    @property
    async def roles_list(self) -> List[Optional[str]]:
        return [role.name for role in await self.roles]

    @property
    async def roles_ids(self) -> List[Optional[int]]:
        return [role.id for role in await self.roles]
