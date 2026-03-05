from fastapi import APIRouter, Depends, Body, Response
from src.di import get_injector, Injector
from ..schemas import UserPublic
from .schemas import UserLoginRequest, LoginResult
from .use_case import UserLogin
from ..config import SESSION_EXPIRATION


router = APIRouter(
    tags=["Users"]
)


@router.post("/login", status_code=200, response_model=UserPublic)
async def user_login(
    response: Response,
    data: UserLoginRequest = Body(...),
    injector: Injector = Depends(get_injector)
):
    use_case: UserLogin = injector.inject(UserLogin)
    result: LoginResult = await use_case.execute(
        email=data.email,
        password=data.password,
        session_expiration=SESSION_EXPIRATION
    )

    response.set_cookie(
        key="session_id",
        value=str(result.session_id),
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=SESSION_EXPIRATION
    )

    return result.user_public



