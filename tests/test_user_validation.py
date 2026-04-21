from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_user_returns_422_when_email_is_invalid():
    response = client.post(
        "/users/",
        json={
            "email": "no_es_email",
            "password": "123456"
        }
    )

    assert response.status_code == 422


def test_register_user_returns_422_when_required_fields_are_missing():
    response = client.post(
        "/users/",
        json={
            "email": "test@test.com"
        }
    )

    assert response.status_code == 422