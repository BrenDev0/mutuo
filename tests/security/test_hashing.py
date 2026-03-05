import pytest
from src.security.bcrypt.hashing import BcryptHashingService

@pytest.fixture
def hashing_service():
    return BcryptHashingService()

def test_hash_for_search(hashing_service):
    email = "test@example.com"
    hashed_email = hashing_service.hash_for_search(email)
    assert hashed_email == hashing_service.hash_for_search(email)
    assert isinstance(hashed_email, str)

def test_hash(hashing_service):
    password = "securepassword"
    hashed_password = hashing_service.hash(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password  

def test_compare(hashing_service):
    password = "securepassword"
    hashed_password = hashing_service.hash(password)
    assert hashing_service.compare(password, hashed_password) is True
    assert hashing_service.compare("wrongpassword", hashed_password) is False

def test_hash_uniqueness(hashing_service):
    password = "securepassword"
    hash1 = hashing_service.hash(password)
    hash2 = hashing_service.hash(password)
    assert hash1 != hash2  