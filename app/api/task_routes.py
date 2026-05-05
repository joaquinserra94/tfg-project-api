from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import app.services.task_service as task_service

from app.core.security import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Listar tareas",
    description="Devuelve el listado de tareas registradas en el sistema. Requiere autenticación mediante token.",
)
def list_tasks_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.list_tasks(db, current_user)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear tarea",
    description="Crea una nueva tarea en el sistema. Requiere autenticación mediante token en el encabezado Authorization.",
)
def create_task_endpoint(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.create_task(db, data, current_user)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Obtener tarea",
    description="Obtiene la información detallada de una tarea concreta a partir de su identificador. Requiere autenticación mediante token.",
)
def get_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.get_task(db, task_id, current_user)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar tarea",
    description="Elimina una tarea existente. Requiere autenticación mediante token en el encabezado Authorization.",
)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service.delete_task(db, task_id, current_user)