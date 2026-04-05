import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login_user():
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"

    user_data = {
        "email": unique_email,
        "password": "clave_segura_123"
    }

    register_response = client.post("/users/", json=user_data)

    assert register_response.status_code in (200, 201)
    register_body = register_response.json()

    assert register_body["email"] == user_data["email"]
    assert "id" in register_body
    assert register_body["is_active"] is True
    assert register_body["is_admin"] is False

    login_response = client.post("/users/login", json=user_data)

    assert login_response.status_code == 200
    login_body = login_response.json()

    assert "access_token" in login_body
    assert login_body["token_type"] == "bearer"