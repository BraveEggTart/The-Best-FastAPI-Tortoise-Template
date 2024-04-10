# from tortoise.signals import Signals


async def listener_pre_save(
    model,
    instance,
    using_db,
    update_fields
):
    ...


async def listener_post_save(
    model,
    instance,
    created,
    using_db,
    update_fields
):
    ...


async def listener_pre_delete(
    model,
    instance,
    using_db
):
    ...


async def listener_post_delete(
    model,
    instance,
    using_db
):
    ...
