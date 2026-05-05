from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Nullable: los proyectos creados antes de esta migración quedan sin owner
    # y solo serán visibles para administradores.
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    tasks = relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )
    owner = relationship("User", back_populates="projects")

# Codigo anterior a la modificación del dia 5/5/26 - en fase de test

'''from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)'''