import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # 👈 AÑADIDO
from sqlalchemy import text

from app.api.project_routes import router as project_router
from app.api.task_routes import router as task_router
from app.api.user_routes import router as user_router
from app.db.session import engine

# 🔹 Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# 🔹 Inicialización de la app
app = FastAPI(
    title="Project Management API",
    description="""
API RESTful para la gestión de proyectos y tareas.

Permite la gestión de usuarios, autenticación mediante token y operaciones CRUD sobre proyectos y tareas.

Incluye paginación, validación de datos y control de acceso.
""",
    version="1.0.0"
)

# 🔥 🔹 CORS (AÑADIDO AQUÍ)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para el TFG (en producción se restringe)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Registro de routers
app.include_router(project_router)
app.include_router(task_router)
app.include_router(user_router)

# 🔹 Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request started - method={request.method} path={request.url.path}")

    response = await call_next(request)

    logger.info(
        f"Request completed - method={request.method} path={request.url.path} status_code={response.status_code}"
    )

    return response

# 🔹 Endpoint raíz
@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "API running"}

# 🔹 Healthcheck de base de datos
@app.get("/health/db")
def check_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("Database healthcheck successful")

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception as e:
        logger.error(f"Database healthcheck failed: {str(e)}")

        return {
            "status": "error",
            "database": "disconnected"
        }