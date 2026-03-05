from src.persistence import AsyncSqlAlchemyDataRepository
from .user_model import SqlAlchemyUser
from ..models import User
    
class SqlAlchemyUserRepository(AsyncSqlAlchemyDataRepository[User, SqlAlchemyUser]):
    def __init__(self):
        super().__init__(SqlAlchemyUser)

    def _to_entity(self, model):
        return User(**model)
    
    def _to_model(self, entity):
        data = entity.model_dump(exclude={"user_id", "created_at"} if not entity.user_id else set())
        return SqlAlchemyUser(**data)