from pydantic import BaseModel
from typing import Optional


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None