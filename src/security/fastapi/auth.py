from fastapi import Request, HTTPException, Depends
from uuid import UUID
from src.di import get_injector, Injector
from src.persistence import AsyncSessionRepository

async def user_authentication(
    request: Request,
    injector: Injector = Depends(get_injector)
) -> UUID:
    """
    User authentication for incoming requests
    Use with Depends() on specific routes
    """
    
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session_repository: AsyncSessionRepository = injector.inject(AsyncSessionRepository)

    session_data = await session_repository.get_session(str(session_id))
    if not session_data:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_id = session_data.get("user_id")
    is_authenticated = session_data.get("is_authenticated")

    if not user_id or not is_authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return UUID(user_id)
  