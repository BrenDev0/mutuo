from src.di.injector import Injector
from .services import (
    EncryptionService,
    HashingService,
    WebTokenService
)

from .bcrypt.hashing import BcryptHashingService
from .fernet.encryption import FernetEncryptionService
from .jwt.web_token import JwtWebTokenService

def register_dependencies(injector: Injector):
    injector.register(EncryptionService, FernetEncryptionService)
    injector.register(HashingService, BcryptHashingService)
    injector.register(WebTokenService, JwtWebTokenService)
    