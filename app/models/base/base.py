from datetime import datetime
from typing import TypeVar, Union, List, Tuple
from collections import defaultdict

from tortoise import fields
from tortoise.models import Model
from tortoise.expressions import F

from app.config import settings

MODEL = TypeVar("MODEL", bound="Model")


class BaseModel(Model):
    id = fields.BigIntField(pk=True, index=True)

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
                values = [
                    await item.to_dict(
                        exclude=relation_exclude[field],
                        m2m=False
                    ) for item in await getattr(self, field).all()
                ]
                result[field] = values
        return result

    class Meta:
        abstract = True


class VersionBaseModel(BaseModel):
    """基于乐观锁的表单超卖控制模型
    """
    version = fields.IntField()

    async def safe_save(self, **kwargs):
        kwargs["version"] = F('version') + 1
        updated_count = await self.filter(id=self.id, version=self.version)\
            .update(**kwargs)

        if updated_count == 0:
            await self.refresh_from_db(fields=["version"])
            await self.safe_save(**kwargs)

    class Meta:
        abstract = True


class UUIDModel:
    uuid = fields.UUIDField(unique=True, pk=False)


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
