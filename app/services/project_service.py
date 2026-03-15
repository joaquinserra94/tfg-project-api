from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate


def create_project(db: Session, project_data: ProjectCreate):
    project = Project(**project_data.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_projects(db: Session):
    return db.query(Project).all()


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()

    if project:
        db.delete(project)
        db.commit()

    return project

def update_project(db: Session, project_id: int, project_data: ProjectCreate):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return None

    project.name = project_data.name
    project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project