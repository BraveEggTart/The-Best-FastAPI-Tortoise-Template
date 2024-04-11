from app.models.admin.users import Users
from app.models.admin.operations import Operations


async def task_record_user_action(
    user: Users, 
    action: str,
    operation: str,
    detail: str,
) -> None:
    await Operations.create(
        user_id=user,
        action=action,
        operation=operation,
        detail=detail,
    )
