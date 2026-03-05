from typing import Optional
from ..schemas import UserConfig


class UpdateUserRequest(UserConfig):
    name: Optional[str] = None
    phone: Optional[str] = None
