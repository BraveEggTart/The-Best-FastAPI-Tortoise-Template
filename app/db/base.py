from datetime import datetime
from typing import TypeVar, Union, List, Tuple, Dict, Optional
from collections import defaultdict

from tortoise import fields
from tortoise.models import Model
from tortoise.expressions import F
from tortoise.signals import pre_save, post_save, pre_delete, post_delete

from app.config import settings

MODEL = TypeVar("MODEL", bound="Model")


class BaseModel(Model):
    # uuid避免并发插入问题
    id = fields.UUIDField(pk=True, index=True)
    # 版本字段避免并发更新问题
    version = fields.IntField(default=0)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    async def to_dict(
        self,
        include: Union[List, Tuple] = [],
        exclude: Union[List, Tuple] = [],
        m2m: bool = False,
    ) -> Union[
        Dict[str, Optional[str]],
        List[Optional[str]]
    ]:
        result = {}
        curr_include, relation_include = self._cut_fields(include, m2m)
        curr_exclude, relation_exclude = self._cut_fields(exclude, m2m)
        curr_remain_field = self._meta.db_fields.difference(set(curr_exclude))
        if len(curr_include) > 0:
            curr_remain_field = curr_remain_field.intersection(curr_include)
        for field in curr_remain_field:
            value = getattr(self, field)
            if isinstance(value, datetime):
                value = value.strftime(settings.DATETIME_FORMAT)
            result[field] = value
        if m2m:
            relation_remain_field = set(self._meta.m2m_fields)\
                .intersection(set(relation_include.keys()))
            for field in relation_remain_field:
                values = [
                    await item.to_dict(
                        include=relation_include.get(field, []),
                        exclude=relation_exclude.get(field, []),
                        m2m=m2m
                    ) for item in await getattr(self, field).all()
                ]
                result[field] = values
        return list(result.values())[0]\
            if len(curr_remain_field) == 1 else result

    def _cut_fields(
        self,
        field_list: Union[List[str], Tuple[str]],
        m2m: bool = False
    ):
        curr_fields = []
        relation_fields = defaultdict(list)
        for item in field_list:
            if '__' not in item:
                curr_fields.append(item)
            elif m2m:
                field, name = item.split("__", 1)
                relation_fields[field].append(name)
        return curr_fields, dict(relation_fields)

    async def safe_save(self, **kwargs):
        kwargs["version"] = F('version') + 1
        updated_count = await self.filter(
            id=self.id,
            version=self.version
        ).update(**kwargs)

        if updated_count == 0:
            await self.refresh_from_db(fields=["version"])
            await self.safe_save(**kwargs)

    class Meta:
        abstract = True


# 定义保存前钩子
@pre_save(BaseModel)
async def pre_save_handler(model, instance, using_db, update_fields):
    ...


# 定义保存后钩子
@post_save(BaseModel)
async def post_save_handler(model, instance, created, using_db, update_fields):
    ...


# 定义删除前钩子
@pre_delete(BaseModel)
async def pre_delete_handler(sender, instance, using_db):
    ...


# 定义删除后钩子
@post_delete(BaseModel)
async def post_delete_handler(sender, instance, using_db):
    ...
