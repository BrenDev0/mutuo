import pytest
from cryptography.fernet import Fernet
from src.security.fernet.encryption import FernetEncryptionService

@pytest.fixture
def encryption_service(monkeypatch):
    test_key = Fernet.generate_key().decode("utf-8")
    monkeypatch.setenv("ENCRYPTION_KEY", test_key)
    return FernetEncryptionService()

def test_encrypt_decrypt_string(encryption_service):
    data = "test_string"
    encrypted = encryption_service.encrypt(data)
    decrypted = encryption_service.decrypt(encrypted)
    assert decrypted == data

def test_encrypt_decrypt_integer(encryption_service):
    data = 12345
    encrypted = encryption_service.encrypt(data)
    decrypted = encryption_service.decrypt(encrypted)
    assert decrypted == str(data)

def test_invalid_key(monkeypatch):
    monkeypatch.delenv("ENCRYPTION_KEY", raising=False)
    with pytest.raises(ValueError, match="Encryption variables not set"):
        FernetEncryptionService()

def test_decrypt_with_wrong_key(encryption_service, monkeypatch):
    data = "test_string"
    encrypted = encryption_service.encrypt(data)

    monkeypatch.setenv("ENCRYPTION_KEY", Fernet.generate_key().decode("utf-8"))
    with pytest.raises(Exception):
        new_service = FernetEncryptionService()
        new_service.decrypt(encrypted)