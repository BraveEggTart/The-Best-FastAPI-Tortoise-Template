from tortoise import fields

from app.models.base.base import BaseModel, TimestampMixin


class Roles(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=30, description="角色名称")
    description = fields.CharField(max_length=30, description="描述", default="")
    apis = fields.ManyToManyField("models.Apis", related_name="roles")

    class Meta:
        table = "roles"
        table_description = "角色信息表"
        ordering = ("id", )
