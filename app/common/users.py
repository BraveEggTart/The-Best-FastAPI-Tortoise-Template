from tortoise import fields
from tortoise.signals import pre_save, post_save, pre_delete, post_delete


from .base import BaseModel, TimestampMixin


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
    password = fields.CharField(
        max_length=100,
        description="密码",
    )

    class Meta:
        table = "users"
        table_description = "用户"
        ordering = ("-id", )


# 定义保存前钩子
@pre_save(Users)
async def user_pre_save_handler(model, instance, using_db, update_fields):
    print(f"将要保存用户 {instance.name}")


# 定义保存后钩子
@post_save(Users)
async def user_post_save_handler(model, instance, created, using_db, update_fields):
    print(f"用户 {instance.name} 已保存")


# 定义删除前钩子
@pre_delete(Users)
async def user_pre_delete_handler(sender, instance, using_db):
    print(f"将要删除用户 {instance.name}")


# 定义删除后钩子
@post_delete(Users)
async def user_post_delete_handler(sender, instance, using_db):
    print(f"用户 {instance.name} 已删除")