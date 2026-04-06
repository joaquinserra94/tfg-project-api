from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=ProjectResponse,
    summary="Crear proyecto",
    description="Crea un nuevo proyecto. Requiere autenticación mediante token en el encabezado Authorization."
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.create_project(db, project)


@router.get(
    "/",
    response_model=list[ProjectResponse],
    summary="Listar proyectos",
    description="Devuelve un listado paginado de proyectos mediante los parámetros skip y limit."
)
def list_projects(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return project_service.get_projects(db, skip=skip, limit=limit)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Obtener proyecto",
    description="Obtiene la información detallada de un proyecto concreto a partir de su identificador."
)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.delete(
    "/{project_id}",
    summary="Eliminar proyecto",
    description="Elimina un proyecto existente. Requiere autenticación mediante token en el encabezado Authorization."
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = project_service.delete_project(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "Project deleted"}


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Actualizar proyecto",
    description="Actualiza la información de un proyecto existente. Requiere autenticación mediante token en el encabezado Authorization."
)
def update_project(
    project_id: int,
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_project = project_service.update_project(db, project_id, project)

    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")

    return updated_project