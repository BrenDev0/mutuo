from fastapi import APIRouter, Depends, Body, Response
from src.di import Injector, get_injector
from ..schemas  import UserPublic
from .schemas import CreateUserRequest, CreateUserResult
from .use_case import CreateUser
from ..config import SESSION_EXPIRATION

router = APIRouter(
    tags=["Users"]
)

@router.post("/", status_code=201, response_model=UserPublic)
async def create_user(
    response: Response,
    data: CreateUserRequest = Body(...),
    injector: Injector = Depends(get_injector)
):
    """
    Create user 

    Verification code must come from users email 

    Raises:
    
    &emsp;429: If max attempts have been reached, must request new code to try again
    
    &emsp;401: If verification fails 

    """
    use_case: CreateUser = injector.inject(CreateUser)  
    result: CreateUserResult = await use_case.execute(
        data=data,
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
