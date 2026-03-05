from src.app import AppException

class ResourceNotFoundException(AppException):
    def __init__(
        self, 
        detail: str = "Resource not found",
        status_code: int = 404
    ):
        super().__init__(detail=detail, status_code=status_code)

class CollisionException(AppException):
    def __init__(self, 
        detail: str = "Duplication found",
        status_code: int  = 409
    ):
        super().__init__(detail, status_code)