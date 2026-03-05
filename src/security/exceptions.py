from src.app import AppException

class ExpiredToken(AppException):
    def __init__(
        self,
        detail: str = "Token expired", 
        status_code: int = 401
    ):
        super().__init__(detail, status_code)

class InvalidToken(AppException):
    def __init__(
        self, 
        detail: str = "Invalid token",
        status_code: int = 401
):      
        super().__init__(detail, status_code)
       

class IncorrectPassword(AppException):
    def __init__(
        self,
        detail: str = "Incorrect password",
        status_code: int = 400
    ):
        super().__init__(detail, status_code)
    

class PermissionsException(AppException):
    def __init__(
        self, 
        detail: str = "Forbidden",
        status_code: int = 403
    ):
        super().__init__(detail, status_code)


class HMACException(Exception):
    def __init__(
        self, 
        detail: str = "HMAC verification failed",
        status_code: int = 403
    ):
        super().__init__(detail, status_code)