from pydantic import BaseModel
from uuid import UUID
from ..schemas import UserConfig, UserPublic

class UserLoginRequest(UserConfig):
    email: str
    password: str

class LoginResult(BaseModel):
    user_public: UserPublic
    session_id: UUID
