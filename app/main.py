from fastapi import FastAPI
from sqlalchemy import text

from app.api.project_routes import router as project_router
from app.db.session import engine

from app.api.task_routes import router as task_router

app = FastAPI(
    title="Project Management API",
    description="API RESTful para gestión de proyectos y tareas",
    version="1.0.0"
)

app.include_router(project_router)
app.include_router(task_router)


@app.get("/")
def root():
    return {"message": "API running"}


@app.get("/health/db")
def check_database():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"message": "Database connection successful"}