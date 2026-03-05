from fastapi import Request, HTTPException, Depends
from src.di import Injector, get_injector
from ..exceptions import (
    ExpiredToken,
    InvalidToken,
)
from ..services import EncryptionService, WebTokenService

def user_verification(
    request: Request,
    injector: Injector = Depends(get_injector)
)-> int:
    """
    User verification for incoming requests
    Use with Depends() on specific routes that require verification code from user email
    """
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unautrhorized. Missing required auth headers")

    token = auth_header.split(" ")[1]
    web_token_service: WebTokenService = injector.inject(WebTokenService)

    try:
        token_payload = web_token_service.decode(token)
        verification_code: str = token_payload.get("verification_code", None)

        if not verification_code:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        encryption: EncryptionService = injector.inject(EncryptionService)

        return int(encryption.decrypt(verification_code))
    
    except (ExpiredToken, InvalidToken, ValueError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    except HTTPException:
        raise

    except Exception:
        raise
    