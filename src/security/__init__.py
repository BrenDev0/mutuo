__version__ = "1.0.0"
__author__ = "BrenDev0"
__description__ = "Security package for app"

from .exceptions import (
    HMACException, 
    IncorrectPassword, 
    InvalidToken, 
    ExpiredToken, 
    PermissionsException
)


from .services import (
    EncryptionService,
    HashingService,
    WebTokenService
)

from .bcrypt.hashing import BcryptHashingService
from .fernet.encryption import FernetEncryptionService
from .jwt.web_token import JwtWebTokenService

from .fastapi.auth import user_authentication
from .fastapi.verify import user_verification
from .fastapi.hmac import verify_hmac

from .utils import get_random_code


__all__ = [
    "HMACException",
    "IncorrectPassword",
    "InvalidToken",
    "ExpiredToken",
    "PermissionsException",

    "EncryptionService",
    "HashingService",
    "WebTokenService",

    "FernetEncryptionService",
    "BcryptHashingService",
    "JwtWebTokenService",

    "user_authentication",
    "verify_hmac",
    "user_verification",

    "get_random_code",
]