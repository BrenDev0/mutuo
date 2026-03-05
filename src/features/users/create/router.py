import json
from fastapi import APIRouter, Depends, Body, Response
from uuid import uuid4
from src.persistence import AsyncSessionRepository
from src.di import Injector, get_injector
from ..schemas  import UserPublic
from .schemas import CreateUserRequest
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
    user = await use_case.execute(
        data=data
    )

    session_repository: AsyncSessionRepository = injector.inject(AsyncSessionRepository)
    
    session_id = uuid4()
    
    session_data = {
        "user_id": str(user.user_id),
        "is_authenticated": True
    }
    
    await session_repository.set_session(
        key=str(session_id),
        value=json.dumps(session_data),
        expire_seconds=SESSION_EXPIRATION
    )

    response.set_cookie(
        key="session_id",
        value=str(session_id),
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=SESSION_EXPIRATION
    )


    return user
