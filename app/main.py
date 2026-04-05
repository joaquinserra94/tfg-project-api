import logging

from fastapi import FastAPI, Request
from sqlalchemy import text

from app.api.project_routes import router as project_router
from app.api.task_routes import router as task_router
from app.api.user_routes import router as user_router
from app.db.session import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Project Management API",
    description="API RESTful para gestión de proyectos y tareas",
    version="1.0.0"
)

app.include_router(project_router)
app.include_router(task_router)
app.include_router(user_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request started - method={request.method} path={request.url.path}")

    response = await call_next(request)

    logger.info(
        f"Request completed - method={request.method} path={request.url.path} status_code={response.status_code}"
    )

    return response


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "API running"}


@app.get("/health/db")
def check_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("Database healthcheck successful")
        return {"message": "Database connection successful"}

    except Exception as e:
        logger.error(f"Database healthcheck failed: {str(e)}")
        return {"message": "Database connection failed"}