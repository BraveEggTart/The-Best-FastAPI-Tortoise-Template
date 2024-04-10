from loguru import logger

from app import api
from app.models.admin.users import Users
from app.models.admin.methods import Methods
from app.models.admin.tags import Tags
from app.models.admin.apis import Apis
from app.models.admin.roles import Roles
from app.utils.password import get_password_hash


async def init_superuser():
    """
    初始化管理员用户
    :param:
    :return:
    """
    check = await Users.exists()
    if not check:
        password = get_password_hash(password="123456")
        admin = await Users.create(
            name="Admin",
            account="admin",
            email="admin@admin.com",
            password=password,
            is_active=True,
            is_superuser=True,
        )
        logger.info("Create Super User Success!")
        super_admin = await Roles.create(
            name="超级管理员",
            description="超级管理员具有最高访问权限及所有接口权限"
        )
        await super_admin.apis.add(*(await Apis.all()))
        await admin.roles.add(super_admin)


async def init_apis():
    """
    初始化API接口
    :param:
    :return:
    """
    await Apis.all().delete()
    for routes in api.api_router.routes:
        record = await Apis.create(
            name=routes.summary,  # type: ignore
            path=routes.path,  # type: ignore
            version=1,
            description=routes.description,  # type: ignore
        )
        for method in routes.methods:  # type: ignore
            method, _ = await Methods.get_or_create(name=method)
            await record.methods.add(method)
        for tag in routes.tags:  # type: ignore
            tag, _ = await Tags.get_or_create(name=tag)
            await record.tags.add(tag)
