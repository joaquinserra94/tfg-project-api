import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_user_and_get_token():
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "clave_segura_123"

    user_data = {
        "email": email,
        "password": password
    }

    client.post("/users/", json=user_data)

    login_response = client.post("/users/login", json=user_data)
    token = login_response.json()["access_token"]

    return token


def test_create_project_authenticated():
    token = create_user_and_get_token()

    project_data = {
        "name": "Proyecto Test",
        "description": "Descripción Test"
    }

    response = client.post(
        "/projects/",
        json=project_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    body = response.json()

    assert body["name"] == "Proyecto Test"
    assert body["description"] == "Descripción Test"
    assert "id" in body


def test_create_project_without_token():
    project_data = {
        "name": "Proyecto Test",
        "description": "Descripción Test"
    }

    response = client.post("/projects/", json=project_data)

    assert response.status_code == 401