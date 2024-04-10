from app.core.ctx import CTX_USER
from app.models.admin.operations import Operations


async def task_record_user_action(
    action: str,
    operation: str,
    detail: str,
) -> None:
    user = CTX_USER.get()
    await Operations.create(
        user_id=user,
        action=action,
        operation=operation,
        detail=detail,
    )
