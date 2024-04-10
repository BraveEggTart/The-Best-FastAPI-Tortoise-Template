from typing import List
from tortoise.models import Model
from tortoise.queryset import QuerySet
from tortoise.exceptions import (
    MultipleObjectsReturned,
)

from app.core.exceptions import InstanceDoesNotExist


async def _execute(self) -> List[Model]:
    instance_list = await self._db.executor_class(
        model=self.model,
        db=self._db,
        prefetch_map=self._prefetch_map,
        prefetch_queries=self._prefetch_queries,
        select_related_idx=self._select_related_idx,
    ).execute_select(self.query, custom_fields=list(self._annotations.keys()))
    if self._single:
        if len(instance_list) == 1:
            return instance_list[0]
        if not instance_list:
            if self._raise_does_not_exist:
                raise InstanceDoesNotExist(
                    f"{self.model._meta.table_description} does not exist"
                )
            return None  # type: ignore
        raise MultipleObjectsReturned(
            "Multiple objects returned, expected exactly one")
    return instance_list


QuerySet._execute = _execute
