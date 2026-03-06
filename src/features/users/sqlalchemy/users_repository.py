from src.persistence import AsyncSqlAlchemyDataRepository
from .user_model import SqlAlchemyUser
from ..models import User
    
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