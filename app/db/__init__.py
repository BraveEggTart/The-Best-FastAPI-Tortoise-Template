import logging

from app.common.users import Users
from app.utils.password import encrypt_aes256
from .base import (
    BaseModel,
    UUIDModel,
    TimestampMixin,
    VersionBaseModel,
)

logger = logging.getLogger(__name__)


async def init_user():
    """
    initial user
    :param:
    :return:
    """
    check = await Users.exists()
    if not check:
        password = encrypt_aes256("123456")
        await Users.create(
            name="Admin",
            account="admin",
            password=password,
        )
        logger.info("Create User Success!")


async def init_db():
    """
    initial db
    :param:
    :return:
    """
    await init_user()


__all__ = [
    "BaseModel",
    "UUIDModel",
    "TimestampMixin",
    "VersionBaseModel",
]