import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def auth_headers():
    email = f"task_{uuid.uuid4().hex[:8]}@example.com"
    password = "clave123"

    register_response = client.post(
        "/users/",
        json={"email": email, "password": password},
    )
    assert register_response.status_code in (200, 201)

    login_response = client.post(
        "/users/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def project_id(auth_headers):
    response = client.post(
        "/projects/",
        headers=auth_headers,
        json={
            "name": "Proyecto Tasks Test",
            "description": "Proyecto para probar tareas",
        },
    )

    assert response.status_code in (200, 201)
    return response.json()["id"]


def test_create_task_authenticated(auth_headers, project_id):
    response = client.post(
        "/tasks/",
        headers=auth_headers,
        json={
            "title": "Tarea integración",
            "description": "Descripción de prueba",
            "status": "pending",
            "project_id": project_id,
        },
    )

    assert response.status_code in (200, 201)

    data = response.json()
    assert data["title"] == "Tarea integración"
    assert data["project_id"] == project_id


def test_list_tasks_authenticated(auth_headers):
    response = client.get(
        "/tasks/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_authenticated(auth_headers, project_id):
    create_response = client.post(
        "/tasks/",
        headers=auth_headers,
        json={
            "title": "Tarea detalle",
            "description": "Descripción detalle",
            "status": "pending",
            "project_id": project_id,
        },
    )

    assert create_response.status_code in (200, 201)

    task_id = create_response.json()["id"]

    get_response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id


def test_delete_task_authenticated(auth_headers, project_id):
    create_response = client.post(
        "/tasks/",
        headers=auth_headers,
        json={
            "title": "Tarea a eliminar",
            "description": "Descripción eliminar",
            "status": "pending",
            "project_id": project_id,
        },
    )

    assert create_response.status_code in (200, 201)

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code in (200, 204)


def test_create_task_without_token_returns_401():
    response = client.post(
        "/tasks/",
        json={
            "title": "Tarea sin token",
            "description": "Debe fallar",
            "status": "pending",
            "project_id": 1,
        },
    )

    assert response.status_code == 401


def test_list_tasks_without_token_returns_401():
    response = client.get("/tasks/")

    assert response.status_code == 401