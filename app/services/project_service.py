from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


def list_projects(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 100,
):
    """Admins ven TODOS los proyectos (incluidos los huérfanos sin owner).
    Usuarios estándar solo ven los suyos."""
    query = db.query(Project)
    if not current_user.is_admin:
        query = query.filter(Project.owner_id == current_user.id)
    return query.offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int, current_user: User) -> Project:
    """Devuelve el proyecto si existe Y el usuario tiene acceso. Lanza 404/403."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Proyecto no encontrado."
        )

    # Admin siempre tiene acceso. Usuario solo si es el dueño.
    if not current_user.is_admin and project.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "No tienes acceso a este proyecto.",
        )
    return project


def create_project(
    db: Session, data: ProjectCreate, current_user: User
) -> Project:
    """El owner es siempre el usuario autenticado que crea el proyecto."""
    project = Project(**data.dict(), owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(
    db: Session,
    project_id: int,
    data: ProjectUpdate,
    current_user: User,
) -> Project:
    project = get_project(db, project_id, current_user)  # ya valida acceso
    for field, value in data.dict(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int, current_user: User):
    project = get_project(db, project_id, current_user)  # ya valida acceso
    db.delete(project)
    db.commit()