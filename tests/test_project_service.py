from unittest.mock import MagicMock

from app.services.project_service import (
    create_project,
    get_project,
    delete_project,
    update_project,
)
from app.schemas.project import ProjectCreate


def test_create_project():
    db = MagicMock()

    project_data = ProjectCreate(
        name="Test Project",
        description="Test Description"
    )

    project = create_project(db, project_data)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

    assert project.name == "Test Project"


def test_get_project_found():
    db = MagicMock()
    mock_project = MagicMock(id=1)

    db.query().filter().first.return_value = mock_project

    result = get_project(db, 1)

    assert result == mock_project


def test_get_project_not_found():
    db = MagicMock()

    db.query().filter().first.return_value = None

    result = get_project(db, 1)

    assert result is None


def test_delete_project_exists():
    db = MagicMock()
    mock_project = MagicMock()

    db.query().filter().first.return_value = mock_project

    result = delete_project(db, 1)

    db.delete.assert_called_once_with(mock_project)
    db.commit.assert_called_once()

    assert result == mock_project


def test_delete_project_not_exists():
    db = MagicMock()

    db.query().filter().first.return_value = None

    result = delete_project(db, 1)

    db.delete.assert_not_called()
    db.commit.assert_not_called()

    assert result is None


def test_update_project_exists():
    db = MagicMock()
    mock_project = MagicMock()

    db.query().filter().first.return_value = mock_project

    project_data = ProjectCreate(
        name="Updated",
        description="Updated Desc"
    )

    result = update_project(db, 1, project_data)

    db.commit.assert_called_once()
    db.refresh.assert_called_once()

    assert result.name == "Updated"


def test_update_project_not_exists():
    db = MagicMock()

    db.query().filter().first.return_value = None

    project_data = ProjectCreate(
        name="Updated",
        description="Updated Desc"
    )

    result = update_project(db, 1, project_data)

    assert result is None