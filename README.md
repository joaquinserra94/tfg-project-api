# Project Management API

API RESTful para la gestión de proyectos y tareas, desarrollada con FastAPI y PostgreSQL como parte del Trabajo Fin de Grado.

---

## Descripción

Este proyecto implementa una API backend que permite gestionar usuarios, proyectos y tareas mediante operaciones CRUD, incorporando autenticación basada en tokens y buenas prácticas de desarrollo software.

La aplicación está diseñada siguiendo una arquitectura modular por capas y ha sido desplegada en un entorno cloud, permitiendo su acceso público.

---

## Tecnologías utilizadas

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migraciones)
- Docker
- Pytest (testing)
- Uvicorn
- Render (despliegue)

---

## Funcionalidades principales

- Registro y autenticación de usuarios
- Gestión de proyectos (crear, listar, actualizar, eliminar)
- Gestión de tareas asociadas a proyectos
- Control de acceso mediante token
- Validación de datos
- Paginación de resultados
- Pruebas unitarias e integración

---

## Estructura del proyecto
app/
├── api/ # Endpoints (rutas)
├── core/ # Configuración y seguridad
├── db/ # Conexión y sesión de base de datos
├── models/ # Modelos ORM
├── schemas/ # Esquemas de validación
├── services/ # Lógica de negocio
├── main.py # Punto de entrada


---

## Ejecución local

### 1. Clonar repositorio

```bash
git https://github.com/joaquinserra94/tfg-project-api.git
cd tfg-project-api

### 2. Ejecutar con Docker
docker compose up --build

### 3. Acceder a la API
API: http://localhost:8000
Documentación: http://localhost:8000/docs

### Testing
docker compose exec api pytest

### Despliegue
La API está desplegada en Render:
https://tfg-project-api.onrender.com
https://tfg-project-api.onrender.com/docs


### Autenticación

El sistema utiliza autenticación basada en tokens.

Flujo:
Registro de usuario
Login → obtención de token
Uso del token en endpoints protegidos

### Calidad del software

Arquitectura por capas
Código modular y tipado
Validaciones robustas
Migraciones reproducibles
Cobertura de tests

### Mejoras futuras

Interfaz frontend
Sistema de roles más avanzado
Notificaciones
Optimización de rendimiento

Autor - Joaquin Serra Prialis
Trabajo Fin de Grado – Ingeniería Informática
