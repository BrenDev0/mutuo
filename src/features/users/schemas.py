from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID
from datetime import datetime
from .models import ProfileType

class UserConfig(BaseModel):
    model_config=ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        str_min_length=1,
        extra="forbid",
        use_enum_values=True
    )

class UserPublic(UserConfig):
    user_id: UUID
    name: str
    phone: str
    email: str
    profile_type: ProfileType
    created_at: datetime