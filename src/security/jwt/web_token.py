import os
import jwt
import logging
import time
from typing import Dict, Any
from ..exceptions import ExpiredToken, InvalidToken
from ..services import WebTokenService
logger = logging.getLogger(__name__)

class JwtWebTokenService(WebTokenService):
    def __init__(self):
        self.__secret = os.getenv("TOKEN_SECRET")
        if not self.__secret:
            raise ValueError("Web token secret not configured")

    def decode(self, token: str):
        try:
            return jwt.decode(token, self.__secret, algorithms=["HS256"])
        
        except jwt.ExpiredSignatureError:
            logger.warning(f"Token expired ::: {token}")
            raise ExpiredToken(f"Token expired ::: {token}")
            
        except jwt.InvalidTokenError:
            logger.warning(f"Invalid token ::: {token}")
            raise InvalidToken(f"Invalid token ::: {token}")
        
    
    def generate(self, payload: Dict[str, Any], expiration: int = 900):
        try:
           
            payload_with_exp = payload.copy()
            payload_with_exp["exp"] = int(time.time()) + expiration

            return jwt.encode(payload_with_exp, self.__secret, algorithm="HS256")
        except Exception as e:
            logger.error("Error generating token:", e)
            raise