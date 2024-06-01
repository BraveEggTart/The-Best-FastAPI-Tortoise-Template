from fastapi import APIRouter, BackgroundTasks

from .users import Users
from .bgtasks import bgtasks_test

router = APIRouter()


@router.get(
    "/user/{id}"
)
async def get_user(
    id: int,
    bgtasks: BackgroundTasks
):
    user = await Users.get(id=id)
    bgtasks.add_task(
        bgtasks_test,
    )
    return await user.to_dict()


@router.delete(
    "/user/{id}"
)
async def delete_user(
    id: int,
):
    user = await Users.get(id=id)
    if user is not None:
        await user.delete()
    return {"detail": "true"}
