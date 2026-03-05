from uuid import UUID
from fastapi import APIRouter, Request, Depends
from src.di import get_injector, Injector
from src.security import user_authentication
from ..schemas import UserPublic
from .use_case import DeleteUser



router = APIRouter(
    tags=["Users"]
)


@router.delete("/", status_code=200, response_model=UserPublic)
async def delete_user(
    request: Request,
    user_id: UUID = Depends(user_authentication),
    injector: Injector = Depends(get_injector)
):
    use_case: DeleteUser = injector.inject(DeleteUser)
    return await use_case.execute(
        user_id=user_id
    )