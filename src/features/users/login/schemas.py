from ..schemas import UserConfig

class UserLoginRequest(UserConfig):
    email: str
    password: str
