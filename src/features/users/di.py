from src.di import Injector
from .repository import UserRepository
from .rules import EmailAvailability
from .sqlalchemy.users_repository import SqlAlchemyUserRepository
from .create.use_case import CreateUser
from .delete.use_case import DeleteUser
from .update.use_case import UpdateUser
from .login.use_case import UserLogin
from .verify_email.use_case import VerifyEmail
from .logout.use_case import UserLogout
from .services import UsersService, EmailAvailabilityService


def register_dependencies(injector: Injector):
    injector.register(UserRepository, SqlAlchemyUserRepository)
    injector.register(UsersService)
    injector.register(CreateUser)
    injector.register(UpdateUser)
    injector.register(UserLogin)
    injector.register(DeleteUser)
    injector.register(VerifyEmail)
    injector.register(UserLogout)
    injector.register(EmailAvailability, EmailAvailabilityService)
    