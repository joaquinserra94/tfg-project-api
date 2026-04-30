from fastapi import APIRouter
from app.db.session import SessionLocal
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

router = APIRouter(prefix="/backup", tags=["backup"])


def clean(obj):
    data = obj.__dict__.copy()
    data.pop("_sa_instance_state", None)
    return data


@router.get("")
def export_backup():
    db = SessionLocal()
    try:
        return {
            "users": [clean(u) for u in db.query(User).all()],
            "projects": [clean(p) for p in db.query(Project).all()],
            "tasks": [clean(t) for t in db.query(Task).all()],
        }
    finally:
        db.close()