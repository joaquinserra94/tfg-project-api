from fastapi import FastAPI

app = FastAPI(
    title="Project Management API",
    description="API RESTful para gestión de proyectos y tareas",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "API running"}