from uuid import UUID
from fastapi import APIRouter, Depends, Body
from src.di import get_injector, Injector
from src.security import user_authentication
from ..schemas import UserPublic
from .schemas import UpdateUserRequest
from .use_case import UpdateUser


router = APIRouter(
    tags=["Users"]
)

@router.patch("/", status_code=200, response_model=UserPublic)
async def update_user(
    data: UpdateUserRequest = Body(...),
    user_id: UUID = Depends(user_authentication),
    injector: Injector = Depends(get_injector)
):
    """
    Update basic user info
    """
    use_case: UpdateUser = injector.inject(UpdateUser)  
    return await use_case.execute(
        user_id=user_id,
        changes=data
    )
