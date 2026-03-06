from uuid import UUID
from src.persistence import AsyncSessionRepository


class UserLogout:
    def __init__(
        self,
        session_repository: AsyncSessionRepository
    ):
        self._session_repository = session_repository

    async def execute(
        self,
        session_id: UUID
    ):
        await self._session_repository.delete_session(key=str(session_id))