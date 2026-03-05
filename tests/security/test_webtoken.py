import pytest
import jwt
import time
from src.security.jwt.web_token import JwtWebTokenService
from src.security.exceptions import ExpiredToken, InvalidToken

@pytest.fixture
def token_service(monkeypatch):
    monkeypatch.setenv("TOKEN_SECRET", "test_secret")
    return JwtWebTokenService()

def test_generate_token(token_service):
    payload = {"user_id": 1}
    token = token_service.generate(payload)
    decoded = jwt.decode(token, "test_secret", algorithms=["HS256"])
    assert decoded["user_id"] == 1
    assert "exp" in decoded

def test_decode_valid_token(token_service):
    payload = {"user_id": 1}
    token = jwt.encode(payload | {"exp": int(time.time()) + 900}, "test_secret", algorithm="HS256")
    decoded = token_service.decode(token)
    assert decoded["user_id"] == 1

def test_decode_expired_token(token_service):
    payload = {"user_id": 1, "exp": int(time.time()) - 1}
    token = jwt.encode(payload, "test_secret", algorithm="HS256")
    with pytest.raises(ExpiredToken):
        token_service.decode(token)

def test_decode_invalid_token(token_service):
    token = "invalid.token.value"
    with pytest.raises(InvalidToken):
        token_service.decode(token)

def test_generate_token_with_custom_expiration(token_service):
    payload = {"user_id": 1}
    token = token_service.generate(payload, expiration=60)
    decoded = jwt.decode(token, "test_secret", algorithms=["HS256"])
    assert decoded["exp"] - int(time.time()) <= 60