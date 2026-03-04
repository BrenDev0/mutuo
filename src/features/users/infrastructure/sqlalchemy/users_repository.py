import uuid
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from src.persistance import SqlAlchemyBase, AsyncSqlAlchemyDataRepository
from ...domain import User

class SqlAlchemyUser(SqlAlchemyBase):
    __tablename__ = "Users"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    email_hash: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    profile_type: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
class SqlAlchemyUserRepository(AsyncSqlAlchemyDataRepository[User, SqlAlchemyUser]):
    def __init__(self):
        super().__init__(SqlAlchemyUser)

    def _to_entity(self, model):
        return User(
            user_id=model.user_id,
            name=model.name,
            phone=model.phone,
            email=model.email,
            email_hash=model.email_hash,
            profile_type=model.profile_type,
            password=model.password,
            created_at=model.created_at
        )
    
    def _to_model(self, entity):
        data = entity.model_dump(exclude={"user_id", "created_at"} if not entity.user_id else set())
        return SqlAlchemyUser(**data)