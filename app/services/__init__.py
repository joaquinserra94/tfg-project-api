from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.project import ProjectCreate, ProjectResponse
import app.services.project_service as project_service