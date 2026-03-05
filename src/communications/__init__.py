__version__ = "1.0.0"
__author__ = "BrenDev0"
__description__ = "Communications package for app"

from .services import EmailService
from .models import Email

__all__ = [
    "Email",
    "EmailService"
]

