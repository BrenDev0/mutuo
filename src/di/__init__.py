__version__ = "1.0.0"
__author__ = "BrenDev0"
__description__ = "Di package for app"


from .injector import Injector
from .fastapi.get_injector import get_injector

__all__ = [
    "Injector",
    "get_injector"
]
