from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate
from app.services.project_service import get_project  # reusa validación


def list_tasks(db: Session, current_user: User):
    """Admins ven todas. Usuarios solo las de sus proyectos."""
    query = db.query(Task).join(Project, Task.project_id == Project.id)
    if not current_user.is_admin:
        query = query.filter(Project.owner_id == current_user.id)
    return query.all()


def get_task(db: Session, task_id: int, current_user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tarea no encontrada.")
    # Hereda permisos del proyecto: get_project lanza 403 si no tienes acceso.
    get_project(db, task.project_id, current_user)
    return task


def create_task(db: Session, data: TaskCreate, current_user: User) -> Task:
    # Verifica acceso al proyecto antes de crear la tarea
    get_project(db, data.project_id, current_user)
    task = Task(**data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, current_user: User):
    task = get_task(db, task_id, current_user)  # ya valida
    db.delete(task)
    db.commit()