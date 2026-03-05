from cryptography.fernet import Fernet
from typing import Union
import os
from ..services import EncryptionService


class FernetEncryptionService(EncryptionService):
    def __init__(self):
        self.__secret_key = os.getenv("ENCRYPTION_KEY")

        if not self.__secret_key:
            raise ValueError("Encryption variables not set")

        self.__fernet = Fernet(self.__secret_key)

    def encrypt(self, data: Union[str, int]) -> str:
        data_str = str(data)
        encrypted = self.__fernet.encrypt(data_str.encode("utf-8"))
        return encrypted.decode("utf-8")

    def decrypt(self, data: str) -> str:
        decrypted = self.__fernet.decrypt(data.encode("utf-8"))
        return decrypted.decode("utf-8")