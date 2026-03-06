from ..schemas import UserConfig
from ..models import ProfileType

class CreateUserRequest(UserConfig):
    verification_code: int
    name: str
    phone: str
    email: str
    password: str
    profile_type: ProfileType

