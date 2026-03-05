from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class User(BaseModel):
    user_id: Optional[UUID] = None
    name: str
    phone: str
    email: str
    email_hash: str
    profile_type: str
    password: str
    created_at: Optional[datetime] = None

