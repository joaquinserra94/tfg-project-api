import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_user_and_get_token():
    email = f"task_{uuid.uuid4().hex[:8]}@example.com"
    password = "clave123"

    register_response = client.post(
        "/users/",
        json={"email": email, "password": password}
    )
    assert register_response.status_code in (200, 201)

    login_response = client.post(
        "/users/login",
        json={"email": email, "password": password}
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return token


def create_project(token):
    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Proyecto Tasks Test",
            "description": "Proyecto para probar tareas"
        }
    )
    assert response.status_code in (200, 201)
    return response.json()["id"]


def test_create_task_authenticated():
    token = create_user_and_get_token()
    project_id = create_project(token)

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Tarea integración",
            "description": "Descripción de prueba",
            "status": "pending",
            "project_id": project_id
        }
    )

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["title"] == "Tarea integración"
    assert data["project_id"] == project_id


def test_create_task_without_token_returns_401():
    response = client.post(
        "/tasks/",
        json={
            "title": "Tarea sin token",
            "description": "Debe fallar",
            "status": "pending",
            "project_id": 1
        }
    )

    assert response.status_code == 401