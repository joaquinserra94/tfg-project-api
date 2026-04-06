from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.services.task_service as task_service

from app.schemas.task import TaskCreate, TaskResponse
from app.db.dependencies import get_db

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    summary="Crear tarea",
    description="Crea una nueva tarea en el sistema. Requiere autenticación mediante token en el encabezado Authorization."
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_service.create_task(db, task)


@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="Listar tareas",
    description="Devuelve el listado de tareas registradas en el sistema."
)
def list_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Obtener tarea",
    description="Obtiene la información detallada de una tarea concreta a partir de su identificador."
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete(
    "/{task_id}",
    summary="Eliminar tarea",
    description="Elimina una tarea existente. Requiere autenticación mediante token en el encabezado Authorization."
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = task_service.delete_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted"}




