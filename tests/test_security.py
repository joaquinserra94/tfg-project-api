from jose import jwt

from app.core.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_returns_different_value():
    password = "mi_clave_segura_123"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert isinstance(hashed_password, str)


def test_verify_password_accepts_valid_password():
    password = "mi_clave_segura_123"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_rejects_invalid_password():
    password = "mi_clave_segura_123"
    hashed_password = hash_password(password)

    assert verify_password("incorrecta", hashed_password) is False


def test_create_access_token_contains_subject():
    token = create_access_token({"sub": "test@example.com"})

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == "test@example.com"
    assert "exp" in payload