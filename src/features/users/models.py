from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

class ProfileType(Enum):
    OWNER = "OWNER"
    RENTER = "RENTER"

class User(BaseModel):
    user_id: Optional[UUID] = None
    name: str
    phone: str
    email: str
    email_hash: str
    profile_type: ProfileType
    password: str
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        use_enum_values=True
    ) 

