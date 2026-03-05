from uuid import UUID
from pydantic import BaseModel
from ..schemas import UserConfig, UserPublic

class CreateUserRequest(UserConfig):
    verification_code: int
    name: str
    phone: str
    email: str
    password: str
    profile_type: str

class CreateUserResult(BaseModel):
    user_public: UserPublic
    session_id: UUID

