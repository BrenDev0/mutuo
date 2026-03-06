from fastapi import APIRouter, Request, Response, Depends
from uuid import UUID
from src.di import Injector, get_injector
from .use_case import UserLogout

router =APIRouter(
    tags=["Users"]
)

@router.post("/logout", status_code=200)
async def logout(
    request: Request,
    response: Response,
    injector: Injector = Depends(get_injector)
):
    session_id = request.cookies.get("session_id")

    if not session_id:
        return 
    
    use_case: UserLogout = injector.inject(UserLogout)
    await use_case.execute(session_id=UUID(session_id))

    response.delete_cookie(
        key="session_id",
        path="/"
    )