from fastapi import APIRouter, Request, Depends, Body
from src.di import Injector, get_injector
from src.security import user_verification
from ..schemas  import UserPublic
from .schemas import CreateUserRequest
from .use_case import CreateUser

router = APIRouter(
    tags=["Users"]
)

@router.post("/", status_code=200, response_model=UserPublic)
async def create_user(
    request: Request,
    data: CreateUserRequest = Body(...),
    verification_code: int = Depends(user_verification),
    injector: Injector = Depends(get_injector)
):
    use_case: CreateUser = injector.inject(CreateUser)  
    return await use_case.execute(
        data=data,
        verification_code=verification_code,
        profile_type="OWNER"
    )
