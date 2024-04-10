from tortoise import fields

from app.models.base.base import BaseModel, TimestampMixin


class Apis(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=30, description="名称")
    path = fields.CharField(max_length=30, description="路径")
    version = fields.IntField(description="版本")
    description = fields.CharField(max_length=30, description="描述", default="")
    tags = fields.ManyToManyField("models.Tags", related_name="apis")
    methods = fields.ManyToManyField("models.Methods", related_name="apis")

    class Meta:
        table = "apis"
        table_description = "API接口表"
        ordering = ("id", )
