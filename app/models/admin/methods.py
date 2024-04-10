from tortoise import fields

from app.models.base.base import BaseModel, TimestampMixin


class Methods(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=30, unique=True, description="名称")

    class Meta:
        table = "methods"
        table_description = "API Method表"
        ordering = ("id", )
