from abc import ABC, abstractmethod
from typing import Union, Dict, Any

class WebTokenService(ABC):
    @abstractmethod
    def decode(
        self,
        token: str
    ):
        raise NotImplementedError
    
    @abstractmethod
    def generate(
        self,
        payload: Dict[str, Any],
        expiration: int = 900
    ) -> str:
        raise NotImplementedError

class HashingService(ABC):
    @abstractmethod
    def hash_for_search(self, data: str) -> str:
       raise NotImplementedError()

    @abstractmethod
    def hash(self, password: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def compare(
        self,
        unhashed: str, 
        hashed: str,
    ) -> bool:
        raise NotImplementedError()
    


class EncryptionService(ABC):
    @abstractmethod
    def encrypt(self, data: Union[str, int]) -> str:
        raise NotImplementedError()

    @abstractmethod
    def decrypt(self, data: str) -> str:
        raise NotImplementedError()