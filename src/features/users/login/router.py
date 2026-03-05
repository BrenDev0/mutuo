from fastapi import APIRouter, Request, Depends, Body
from src.di import get_injector, Injector
from ..schemas import UserPublic
from .schemas import UserLoginRequest
from .use_case import UserLogin


router = APIRouter(
    tags=["Users"]
)

@router.post("/login", status_code=200, response_model=UserPublic)
def user_login(
    request: Request,
    data: UserLoginRequest = Body(...),
    injector: Injector = Depends(get_injector)
):
    use_case: UserLogin = injector.inject(UserLogin)
    return use_case.execute(
        email=data.email,
        password=data.password
    )

