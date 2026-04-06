from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
import app.services.user_service as user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponse,
    summary="Registrar usuario",
    description="Crea un nuevo usuario en el sistema a partir de un correo electrónico y una contraseña."
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return user_service.create_user(db, user)


@router.post(
    "/login",
    summary="Autenticación de usuario",
    description="Permite a un usuario autenticarse y obtener un token de acceso."
)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(
        db,
        user_credentials.email,
        user_credentials.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }