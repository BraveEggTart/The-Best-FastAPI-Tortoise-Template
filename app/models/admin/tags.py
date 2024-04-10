from tortoise import fields

from app.models.base.base import BaseModel, TimestampMixin


class Tags(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=30, unique=True, description="名称")
    description = fields.CharField(max_length=30, description="描述", default="")

    class Meta:
        table = "tags"
        table_description = "API标签表"
        ordering = ("id", )
