from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine

app = FastAPI(
    title="Project Management API",
    description="API RESTful para gestión de proyectos y tareas",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "API running"}


@app.get("/health/db")
def check_database():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"message": "Database connection successful"}