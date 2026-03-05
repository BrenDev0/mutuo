from fastapi import Request, HTTPException, Depends
from uuid import UUID
from src.di import get_injector, Injector
from ..exceptions import (
    ExpiredToken, 
    InvalidToken
)
from ..services import WebTokenService


def user_authentication(
    request: Request,
    injector: Injector = Depends(get_injector)
) -> UUID:
    """
    User authentication for incoming requests
    Use with Depends() on specific routes
    """
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unautrhorized. Missing required auth headers")

    token = auth_header.split(" ")[1]
    web_token_service: WebTokenService = injector.inject(WebTokenService)

    try:
        token_payload = web_token_service.decode(token)
        user_id: UUID = token_payload.get("user_id", None)

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return user_id
    
    except (ExpiredToken, InvalidToken, ValueError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    except HTTPException:
        raise