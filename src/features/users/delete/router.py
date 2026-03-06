from uuid import UUID
from fastapi import APIRouter, Request, Depends, Response
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
    response: Response,
    user_id: UUID = Depends(user_authentication),
    injector: Injector = Depends(get_injector)
):
    """
    Delete user 
    """
    session_id = request.cookies.get("session_id")
    use_case: DeleteUser = injector.inject(DeleteUser)
    
    deleted_user = await use_case.execute(
        session_id=UUID(session_id),
        user_id=user_id
    )

    response.delete_cookie(
        key="session_id",
        path="/"
    )

    return deleted_user