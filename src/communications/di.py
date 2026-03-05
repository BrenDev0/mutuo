from src.di import Injector
from .services import EmailService

def register_dependencies(injector: Injector):
    injector.register(EmailService)