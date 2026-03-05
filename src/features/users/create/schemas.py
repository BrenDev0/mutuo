from ..schemas import UserConfig

class CreateUserRequest(UserConfig):
    verification_code: int
    name: str
    phone: str
    email: str
    password: str

