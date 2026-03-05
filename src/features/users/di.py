from src.di import Injector
from .repository import UserRepository
from .rules import EmailAvailability
from .sqlalchemy.users_repository import SqlAlchemyUserRepository
from .create.use_case import CreateUser
from .delete.use_case import DeleteUser
from .update.use_case import UpdateUser
from .login.use_case import UserLogin
from .services import UsersService, EmailAvailabilityService


def register_dependencies(injector: Injector):
    injector.register(UserRepository, SqlAlchemyUserRepository)
    injector.register(UsersService)
    injector.register(CreateUser)
    injector.register(UpdateUser)
    injector.register(UserLogin)
    injector.register(DeleteUser)
    injector.register(EmailAvailability, EmailAvailabilityService)
    